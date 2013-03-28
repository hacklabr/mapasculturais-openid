$(document).ready(function() {
    // quando o usuário muda um dos campos da sua ocupação atualiza a lista de opções do campo seguinte
    // e desabilita os demais campos que estão abaixo na hierarquia
    $('.user_occupation').change(function() {
        // pega o select seguinte que é controlado pelo que foi alterado
        var childSelect = $(this).parent().parent().nextAll().find('.user_occupation').first();
        
        if (childSelect.length > 0) {
            $('body').css('cursor', 'wait');
            $.getJSON('/occupations/?parent=' + $(this).val(), function(data) {
                childSelect.children().remove();
                $.each(data, function(key, val) {
                    childSelect.append($("<option></option>").attr("value", key).text(val));
                })
                childSelect.removeAttr('disabled');
                
                // limpa e desabilita todos os selects que estão abaixo do childSelect na hierarquia
                childSelect.parent().parent().nextAll().find('.user_occupation').each(function(key, e) {
                    if (!$(e).attr('disabled')) {
                        $(e).children().remove();
                        $(e).append($("<option></option>").text('---------'));
                        $(e).attr('disabled', 'disabled');
                    }
                });
                $('body').css('cursor', 'auto');
            });
        }
    });
});