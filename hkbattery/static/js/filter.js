// compare button and checkbox states
$(document).ready(function() {
    var btn = 'input[name="action"]'
    var cbox = 'input[name="compare"]'
    var mincount = 2
    var maxcount = 5
    $(btn).prop('disabled', true);
    $(cbox).click(function() {
        var cboxcount = $(cbox+':checked').length
        if (cboxcount == 0){
          $(btn).prop('value', 'Compare')
        } else {
          $(btn).prop('value', 'Compare ['+cboxcount+'/'+maxcount+']')
        }
        if (cboxcount < mincount){
            $(btn).prop('disabled', true);
        } else {
            $(btn).prop('disabled', false);
        };
        var bol = cboxcount >= maxcount;
        $(cbox).not(':checked').prop('disabled', bol);
    });
});
// show/hide filter panel
$(document).ready(function() {
    setTimeout('$("#sidebar").toggleClass("collapsed");\
        $("#content").toggleClass("col-md-12 col-md-10")', 1000)
    $('.toggle-sidebar').click(function() {
        $('#sidebar').toggleClass('collapsed');
        $('#content').toggleClass('col-md-12 col-md-10');
        return false;
    });
});
// column sorting
$(document).ready(function() {
    $('#row-main').on('click', '.sortable a', function(event) {
        event.preventDefault();
        $('#table').load($(this).prop('href') + ' #table')
    });
});
// pagination
$(document).ready(function() {
    $('#row-main').on('click', '.pagination a[href*="page"]', function(event) {
        event.preventDefault();
        $('#table').load($(this).prop('href') + ' #table')
        $(window).scrollTop($('body').offset().top);
    });
});
// filtering
$('#filter').on('click', 'input[name="filter"]', function(event) {
    event.preventDefault();
    apply_filter('filter');
});

function apply_filter(action) {
    var data = {}
    data[action] = action
    $('input[class*="textinput textInput form-control"]').each(function(i, el) {
        var name = $(el).prop('name')
        if (name == 'name') {
            data[name] = $(el).val();
        } else {
            data[name.slice(0,-1) + '0'] = $(el).data('slider').getValue()[0];
            data[name] = $(el).data('slider').getValue()[1];
        }
    });
    console.log(data)
    $.ajax({
        url: window.location.href,
        type: 'get',
        data: data,
        success: function(data) {
            $('#content').html($('#content', data).html());
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
};
