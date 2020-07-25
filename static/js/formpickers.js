(function($) {
  'use strict';
  if ($("#timepicker-example").length) {
    $('#timepicker-example').datetimepicker({
      format: 'LT'
    });
  }
  if ($(".color-picker").length) {
    $('.color-picker').asColorPicker();
  }
  if ($("#datepicker-popup").length) {
    $('#datepicker-popup').datepicker({
      format: 'dd/mm/yyyy',
      enableOnReadonly: true,
      todayHighlight: true,
      autoclose: true
    });
  }
  if ($("#inline-datepicker").length) {
    $('#inline-datepicker').datepicker({
      format: 'dd/mm/yyyy',
      enableOnReadonly: true,
      todayHighlight: true,
      autoclose: true
    });
  }
  if ($(".datepicker-autoclose").length) {
    $('.datepicker-autoclose').datepicker({
      autoclose: true,
      format: 'dd/mm/yyyy'
    });
  }
  if($('.input-daterange').length) {
    $('.input-daterange input').each(function() {
      $(this).datepicker('clearDates');
    });
    $('.input-daterange').datepicker({
      format: 'dd/mm/yyyy'
    });
  }
})(jQuery);