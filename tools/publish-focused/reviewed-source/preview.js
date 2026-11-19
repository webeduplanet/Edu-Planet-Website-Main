(function () {
  'use strict';
  document.addEventListener('change', function (event) {
    if (event.target.matches('.preview-page-picker select')) window.location.href = event.target.value;
  });
  document.addEventListener('click', function (event) {
    var opener = event.target.closest('[data-open-dialog]');
    if (opener) {
      event.preventDefault();
      document.getElementById(opener.dataset.openDialog).showModal();
      return;
    }
    var application = event.target.closest('a[href="#application-preview"]');
    if (application) {
      event.preventDefault();
      document.getElementById('application-preview').showModal();
      return;
    }
    var closer = event.target.closest('[data-close-dialog]');
    if (closer) closer.closest('dialog').close();
  });
  function openLinkedFeeDetails() {
    var dialog = document.getElementById(window.location.hash.slice(1));
    if (dialog && dialog.matches('dialog.fee-info-dialog') && !dialog.open) dialog.showModal();
  }
  window.addEventListener('hashchange', openLinkedFeeDetails);
  openLinkedFeeDetails();
  document.querySelectorAll('dialog').forEach(function (dialog) {
    dialog.addEventListener('click', function (event) {
      if (event.target !== dialog) return;
      var r = dialog.getBoundingClientRect();
      if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
    });
  });
})();
