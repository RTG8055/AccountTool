(function($) {
  'use strict';
  $(function() {

    //basic config
    if ($("#js-grid").length) {
      $("#js-grid").jsGrid({
        height: "500px",
        width: "100%",
        filtering: true,
        editing: true,
        inserting: true,
        sorting: true,
        paging: true,
        autoload: true,
        pageSize: 15,
        pageButtonCount: 5,
        deleteConfirm: "Do you really want to delete the client?",
        data: db.clients,
        fields: [{
            name: "Name",
            type: "text",
            width: 150
          },
          {
            name: "Age",
            type: "number",
            width: 50
          },
          {
            name: "Address",
            type: "text",
            width: 200
          },
          {
            name: "Country",
            type: "select",
            items: db.countries,
            valueField: "Id",
            textField: "Name"
          },
          {
            name: "Married",
            title: "Is Married",
            itemTemplate: function(value, item) {
              return $("<div>")
                .addClass("form-check mt-0")
                .append(
                  $("<label>").addClass("form-check-label")
                  .append(
                    $("<input>").attr("type", "checkbox")
                    .addClass("form-check-input")
                    .attr("checked", value || item.Checked)
                    .on("change", function() {
                      item.Checked = $(this).is(":checked");
                    })
                  )
                  .append('<i class="input-helper"></i>')
                );
            }
          },
          {
            type: "control"
          }
        ]
      });
    }

    if ($("#daily-inventory").length) {
      console.log(db.items);
      $("#daily-inventory").jsGrid({
        height: "500px",
        width: "100%",

        sorting: true,
        paging: true,

        data: db.items,

        fields: [{
            name: "Invoice Date",
            type: "text",
            width: 50
          },
          {
            name: "Item Name",
            type: "text",
            width: 50
          },
            {
            name: "Party Name",
            type: "text",
            width: 50
          },
            {
            name: "Dispatch Quantity in kGs",
            type: "text",
            width: 75
          },
            {
            name: "Received Quantity in kGs",
            type: "text",
            width: 75
          }
        ]
      });
    }

    //Static
    if ($("#js-grid-static").length) {
      console.log(db.items);
      $("#js-grid-static").jsGrid({
        height: "500px",
        width: "100%",

        sorting: true,
        paging: true,

        data: db.items,

        fields: [{
            name: "Item Name",
            type: "text",
            width: 100
          },
          {
            name: "Current Quantity in kGs",
            type: "text",
            width: 100
          }
        ]
      });
    }

    if ($("#sort").length) {
      $("#sort").on("click", function() {
        var field = $("#sortingField").val();
        $("#js-grid-sortable").jsGrid("sort", field);
      });
    }

  });
})(jQuery);