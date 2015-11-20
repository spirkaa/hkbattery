// show/hide filter panel
$(document).ready(function() {
    setTimeout('$("#sidebar").toggleClass("collapsed");\
        $("#content").toggleClass("col-md-12 col-md-10");', 1000)
    $(".toggle-sidebar").click(function() {
        $("#sidebar").toggleClass("collapsed");
        $("#content").toggleClass("col-md-12 col-md-10");
        return false;
    });
});
// column sorting
$(document).ready(function() {
    $('#row-main').on('click', '.sortable a', function(event) {
        event.preventDefault();
        $('#content').load($(this).attr('href') + ' #table')
    });
});
// pagination
$(document).ready(function() {
    $('#row-main').on('click', '.pagination a[href*="page"]', function(event) {
        event.preventDefault();
        $('#content').load($(this).attr('href') + ' #table')
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
        var name = $(el).attr('name')
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
