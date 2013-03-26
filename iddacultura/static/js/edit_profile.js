$(document).ready(function() {
    $('.user_occupation').change(function() {
        // pega o select seguinte que é controlado pelo que foi alterado
        var childSelect = $(this).parent().parent().nextAll().find('.user_occupation').first()
        
        if (childSelect.length > 0) {
            $('body').css('cursor', 'wait');
            $.getJSON('/occupations/?parent=' + $(this).val(), function(data) {
                childSelect.children().remove();
                $.each(data, function(key, val) {
                    childSelect.append($("<option></option>").attr("value", key).text(val));
                })
                childSelect.removeAttr('disabled');
                $('body').css('cursor', 'auto');
            });
        }
    });
});