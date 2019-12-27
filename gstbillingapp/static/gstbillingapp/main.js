var invoice_item_row_counter = 1

function add_invoice_item_row() {
    old_item_row_count = invoice_item_row_counter
    invoice_item_row_counter++;

    $('#invoice-form-items-table-body >tr:last').clone(true).insertAfter('#invoice-form-items-table-body >tr:last');
    $('#invoice-form-items-table-body >tr:last input').val('');

    $('#invoice-form-items-table-body >tr:last td')[0].innerHTML = invoice_item_row_counter
    
    // newname = $('#invoice-form-items-table-body >tr:last input').attr('name', function(i, val){newval = val.replace(old_item_row_count, invoice_item_row_counter); return newval;})
}


$(document).ready(function() {

    $("#invoice-form-addrow").click(function(event) {
       event.preventDefault();
       add_invoice_item_row();
    });

    
});
