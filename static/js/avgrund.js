(function($) {
  'use strict';
  $(function() {
    $('#show').avgrund({
      height: 1000,
      holderClass: 'custom',
      showClose: true,
      showCloseText: 'x',
      onBlurContainer: '.container-scroller',
      template: '<form class="form-sample" action="/addparty" method="post" id="addPartyForm">' +
                	'<div class="form-group">' +
						          '<label for="party">Party Name</label>' +
	                    '<input type="text" class="form-control" name="party" placeholder="Party Name" required>' +
                  '</div>' +
                  '<div class="form-group">' +
                      '<label for="type">Party Type</label>' +
                      '<select name="type" class="form-control" required>' +
                        '<option value="debtor">Customer</option>' +
                        '<option value="creditor">Supplier</option>' +
                      '</select>' +
                  '</div>' +
                  '<div class="form-group">' +
						          '<label for="address">Address</label>' +
                    	 '<textarea name="address" class="form-control" form="addPartyForm" placeholder="address"></textarea>' +
                  '</div>' +
                  '<div class="form-group">' +
                      '<label for="balance">Opening Balance</label>' +
                      '<input type="real" class="form-control" name="balance" placeholder="Opening Balance" step="0.01" required>' +
                  '</div>' +
                    '<button type="submit" class="btn btn-gradient-primary mb-2">Submit</button>' +
                  '</form>'
    });
  })
})(jQuery);