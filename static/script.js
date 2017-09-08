
$(document).ready(function(){

 $("#myModal").draggable({
      handle: ".modal-header"
  });

$('.openall').click(function(){
  $('.panel-collapse:not(".in")')
    .collapse('show');
});

$('.closeall').click(function(){
  $('.panel-collapse')
    .collapse('hide');
});



    $('.filterable .btn-filter').click(function(){
        var $panel = $(this).parents('.filterable'),
        $filters = $panel.find('.filters input'),
        $tbody = $panel.find('.table tbody');
        if ($filters.prop('disabled') == true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    $('.filterable .filters input').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var $input = $(this),
        inputContent = $input.val().toLowerCase(),
        $panel = $input.parents('.filterable'),
        column = $panel.find('.filters th').index($input.parents('th')),
        $table = $panel.find('.table'),
        $rows = $table.find('tbody tr');
        /* Dirtiest filter function ever ;) */
        var $filteredRows = $rows.filter(function(){
            var value = $(this).find('td').eq(column).text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
        }
    });

var table = $('#myTable').DataTable({
  "language":{
      "lengthMenu":"Visualizza _MENU_ elementi per pagina",
      "search":         "Search:",
      "zeroRecords":    "Nessun quesito Bebras trovato",
      "paginate": {
          "first":      "First",
          "last":       "Last",
          "next":       "Successivo",
          "previous":   "Precedente"
        },
      },
      initComplete: function () {
            this.api().columns(1).every( function () {
                var column = this;
                var select = $('#annoSearch')
                
                select.append( '<option value=""></option>' )
                    
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );

           this.api().columns(2).every( function () {
                var column = this;
                var select = $('#categoriaSearch')
                select.append( '<option value=""></option>' )
                  
                    select.append( '<option value="KiloBebras (8-10anni)">KiloBebras (8-10anni)</option>' )
                    select.append( '<option value="MegaBebras (10-12anni)">MegaBebras (10-12anni)</option>' )
                    select.append( '<option value="GigaBebras (12-13anni)">GigaBebras (12-13anni)</option>' )
                    select.append( '<option value="TeraBebras (13-15anni)">TeraBebras (13-15anni)</option>' )
                    select.append( '<option value="PetaBebras (15-18anni)">PetaBebras (15-18anni)</option>' )
                
                  .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                          
                        );
 
                        column
                            .search( val ? ''+val+'' : '', true, false )
                            .draw();
                    } );
 
                
            } );

        },
});



$('#titoloSearch').on( 'keyup', function () {
    table
        .columns( 0 )
        .search( this.value )
        .draw();
} );


 
});

