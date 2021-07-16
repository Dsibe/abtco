import json
import itertools
from django.views.decorators.csrf import csrf_exempt
import datetime
import calendar
import traceback
from django.contrib.auth.decorators import login_required
import os
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
from django.shortcuts import render
from django.http import HttpResponse

from sellapp.models import License, Machine
from shop.models import App


def get_key(password, salt):
    password = password.encode()
    salt = salt.encode()

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100_000,
                     backend=default_backend())
    return Fernet(urlsafe_b64encode(kdf.derive(password)))


def encrypt(message, fernet):
    if isinstance(message, str):
        message = message.encode()

    return fernet.encrypt(message)


def decrypt(data, fernet):
    return fernet.decrypt(data).decode()


def debug_env_var(name):
    try:
        with open(
                rf'D:\libraries\Desktop\Dj\env\Scripts\app\abtco_env\{name}.txt'
        ) as file:
            return file.read()
    except:
        pass


def get_app_private_keys(app):
    private_creds = app.private_creds
    private_creds = json.loads(private_creds)

    private_fernets = {}
    for version, password, salt in private_creds:
        key_name = f'{app.name_id}_v{version}'
        fernet = get_key(password, salt)
        private_fernets[key_name] = fernet

    return tuple(private_fernets.items())


public_password = os.environ.get('public_password',
                                 debug_env_var('public_password'))

public_salt = os.environ.get('public_salt', debug_env_var('public_salt'))
public_fernet = get_key(public_password, public_salt)

apps = App.objects.all()
all_private_fernets = [get_app_private_keys(app) for app in apps]
all_private_fernets = list(itertools.chain(*all_private_fernets))
all_private_fernets = dict(all_private_fernets)


def decrypt_code(product_name, version, encrypted_code):
    # try:
    key_name = f'{product_name}_v{version}'
    fernet = all_private_fernets.get(key_name)
    print(all_private_fernets.keys(), key_name)
    print(fernet)

    encrypted_code = f'gAAAAAB{encrypted_code}'
    encrypted_code = encrypted_code.encode()
    decrypted_code = decrypt(encrypted_code, fernet)
    return decrypted_code
    # except:
    #     return 'error'


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def is_license_valid(request, args, code_mode=False):
    print()
    print('is_license_valid')

    try:
        args_decrypted = decrypt(args.encode(), public_fernet)
    except InvalidToken:
        return 'error'

    args = args_decrypted.split('/')

    if code_mode:
        username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, product_name, encrypted_code, app_version = args
    else:
        username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, product_name, app_version = args

    try:
        print('license_key', license_key)

        license = License.objects.filter(key=license_key).first()
        if license.user.username != username:
            print('License username doesnt match')
            return 'License not found, maximum machines limit is reached, or machine is blacklisted by an owner of the license.'

        if license.product.name_id != product_name:
            print(len(license.product.name_id), len(product_name))
            print('License product name doesnt match')
            return 'Product name invalid.'

        period = license.expiration

        if period:
            expiration_date = add_months(license.creation_date, period)
            print('now', datetime.date.today())
            print('expiration_date', expiration_date)

            if datetime.date.today() > expiration_date:
                license.delete()
                return 'License expired'

        allowed_machines = license.machine_set.all().filter(
            is_blacklisted=False)

        banned_machines = license.machine_set.all().filter(is_blacklisted=True)

        hardware_id = f'{bios_sn}, {csproduct}, {mac_id}'
        info = f'{system} {version}, {processor}'
        current_machine = None

        print('hardware_id', hardware_id)
        print('info', info)
        print('model', model)

        try:
            print('Trying to find existing machine')
            # If it's existing machine, update last login time
            current_machines = allowed_machines.order_by('-last_login')
            current_machines = allowed_machines.filter(hardware_id=hardware_id,
                                                       model=model,
                                                       info=info)
            current_machine = current_machines.first()
            current_machine.update_last_login_time()

            print('Found machine')
            print('hardware_id', hardware_id)
            print('info', info)
            print('model', model)

        except Exception as e:
            print('No machine found')
            print(e)

            banned_machines = banned_machines.order_by('-last_login')
            banned_machines = banned_machines.filter(hardware_id=hardware_id,
                                                     model=model,
                                                     info=info)
            current_machine = banned_machines.first()
            if current_machine is not None:
                return 'Owner of the license banned this machine.'

        try:
            if current_machine is None:
                print('Creating new machine')

                if len(allowed_machines) < license.max_machines_limit:
                    print('Under limit')
                    new_machine = Machine()
                    new_machine.create_machine(hardware_id, info, model, False,
                                               license)
                current_machine = new_machine

                print('hardware_id', hardware_id)
                print('info', info)
                print('model', model)
                print('Created new machine!')
        except Exception as e:
            print('Too many machines')
            return 'Maximum machines limit reached on this license.'

        if current_machine is not None:
            if code_mode:
                return product_name, app_version, encrypted_code

            return 'success'

    except Exception as e:
        print(e)
        traceback.format_exc()
        # except (License.DoesNotExist, Machine.DoesNotExist) as e:

    print('No license found: ERROR')
    return 'License not found, maximum machines limit is reached, or machine is blacklisted by an owner of the license.'


def license_check(request, args):
    print('license_check')

    result = is_license_valid(request, args)
    if result == 'success':
        print('OK!')
        print('\n' * 3)
        return HttpResponse('ok')

    print('Here')
    print(result)
    return HttpResponse(result)


@csrf_exempt
def decrypt_code_with_license(request):
    print('decrypt_code_with_license')

    args = request.POST.get('args', '')

    try:
        product_name, app_version, encrypted_code = is_license_valid(
            request, args, code_mode=True)
        print('Decrypt code')
        decrypted_code = decrypt_code(product_name, app_version,
                                      encrypted_code)
        print('\n' * 3)
        print('decrypted_code', decrypted_code)
        return HttpResponse(decrypted_code)
    except Exception as e:
        print('Exception', e)
        return HttpResponse('error occured')
        pass


def render_machines(machines):
    return [(
        machine.id,
        machine.info,
        machine.model,
        machine.last_login,
    ) for machine in machines]


@login_required
def view_machines(request, license_id):
    try:
        user = request.user
        license = License.objects.filter(id=license_id).first()
    except:
        return HttpResponse('Error')

    key = license.key
    key = f'{key[:8]}{"*" * 15}'

    allowed_machines = license.machine_set.all().filter(is_blacklisted=False)
    banned_machines = license.machine_set.all().filter(is_blacklisted=True)

    rendered_allowed_machines = render_machines(allowed_machines)
    rendered_banned_machines = render_machines(banned_machines)

    context = {
        'key': key,
        'allowed_machines': rendered_allowed_machines,
        'banned_machines': rendered_banned_machines,
        'license': license,
    }

    return render(request, 'shop/view_machines.html', context=context)


def ban_machine(request, machine_id):
    user = request.user

    machine = Machine.objects.filter(id=machine_id).first()
    machine_user = machine.license.user

    if machine_user == user:
        machine.is_blacklisted = True
        machine.save()
        return HttpResponse('true')

    return HttpResponse('"Error ocurred. Refresh page and try again, please."')


def unban_machine(request, machine_id):
    user = request.user

    machine = Machine.objects.filter(id=machine_id).first()
    machine_user = machine.license.user

    if machine_user == user:
        user_allowed_machines = machine.license.machine_set.filter(
            is_blacklisted=False)
        if len(user_allowed_machines) < machine.license.max_machines_limit:
            machine.is_blacklisted = False
            machine.save()
            return HttpResponse('true')

        return HttpResponse(
            f'"Maximum machines limit is reached. Current limit: {machine.license.max_machines_limit}"'
        )

    return HttpResponse('"Error ocurred. Refresh page and try again, please."')
