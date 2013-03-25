$(document).ready(function() {
    $('#id_user_occupation_primary').change(function() {
        $('body').css('cursor', 'wait');
        $.getJSON('/occupations/?parent=' + $(this).val(), function(data) {
            $('#id_user_occupation_secondary').children().remove();
            $.each(data, function(key, val) {
                $('#id_user_occupation_secondary').append($("<option></option>").attr("value", key).text(val));
            })
            $('body').css('cursor', 'auto');
        });
    });
});