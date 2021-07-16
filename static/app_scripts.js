function show(id) {
  obj = document.getElementById(id);

  obj.classList.add('visible', 'fade-in');
  obj.classList.remove('invisible');
}


function showWindow(id) {
  allVisibleWindows = document.getElementsByClassName('visible');

  for (var visibleI = 0; visibleI < allVisibleWindows.length; visibleI++) {
    hideId = allVisibleWindows[visibleI].id;

    if (hideId != id) {
      hide(hideId);
    }
  }

  show(id);
}

function hide(id) {
  obj = document.getElementById(id);

  obj.classList.add('invisible');
  obj.classList.remove('visible', 'fade-in');
}

function handlePricingBtn(appNameId, pricingId, period, machinesAmount) {
  window.location.href =
    `/buy-license/${appNameId}/${pricingId}/${period}/${machinesAmount}`;
}


function handleCustomPricingBtn(appNameId, pricingId) {
  period = document.getElementById('custom-period').value;
  machinesAmount = document.getElementById('custom-machines-amount').value;
  handlePricingBtn(appNameId, pricingId, period, machinesAmount);
}
