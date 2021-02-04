import pyperclip

text = pyperclip.paste()
text = text.replace('src="images/', 'src="{% static "')
text = text.replace('.png"', '.png" %}"')
pyperclip.copy(text)
