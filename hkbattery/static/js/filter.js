setSlider()
    // range sliders init
function setSlider() {
    var sldr = ['price', 'ru_stock', 's_config', 'capacity', 'weight', 'discharge']
    $.each(sldr, function(k, v) {
        $("#" + v).slider({});
        console.log("#" + v)
    });
}
// filtering
$('#filter-control').on('click', 'input[name="filter"]', function(event) {
    event.preventDefault();
    $('input[class*="span2"]').each(function(i, el) {
        console.log($(el).attr('id') + ': ' + $(el).data('slider').getValue()[0])
    });
    run_process('filter');
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

function run_process(action) {
    var data = {}
    data[action] = action
    $('input[class*="form-control"]').each(function(i, el) {
        if ($(el).attr('id') == 'name') {
            data[$(el).attr('id')] = $(el).val();
        } else {
            data[$(el).attr('id') + '_0'] = $(el).data('slider').getValue()[0];
            data[$(el).attr('id') + '_1'] = $(el).data('slider').getValue()[1];
        }
    });
    console.log(data)
    $.ajax({
        url: window.location.href,
        type: 'get',
        data: data,

        // handle a successful response
        success: function(data) {
            $('#content').html($('#content', data).html());
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            $('#messages').append("<div class='alert alert-danger fade in'>Oops! We have encountered an error: " + errmsg +
                " <button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
