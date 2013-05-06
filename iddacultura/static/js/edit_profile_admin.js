//TODO: esse script é uma cópia do edit_profile.js adaptado para o HTML do admin do django.
//      é possível que exista uma maneira melhor para juntar os dois em um só.
jQuery(document).ready(function() {
    // quando o usuário muda um dos campos da sua ocupação atualiza a lista de opções do campo seguinte
    // e desabilita os demais campos que estão abaixo na hierarquia
    $("[name^='userprofile-0-user_occupation_']").change(function() {
        // pega o select seguinte que é controlado pelo que foi alterado
        var childSelect = $(this).parent().parent().nextAll().find("[name^='userprofile-0-user_occupation_']").first();

        if (childSelect.length > 0) {
            $('body').css('cursor', 'wait');
            $.getJSON('/occupations/?parent=' + $(this).val(), function(data) {
                childSelect.children().remove();
                $.each(data, function(key, val) {
                    childSelect.append($("<option></option>").attr("value", key).text(val));
                })
                childSelect.removeAttr('disabled');

                // limpa e desabilita todos os selects que estão abaixo do childSelect na hierarquia
                childSelect.parent().parent().nextAll().find("[name^='userprofile-0-user_occupation_']").each(function(key, e) {
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

    // desabilita um campo de seleção de ocupação se o anterior não estiver selecionado
    $("[name^='userprofile-0-user_occupation_']").each(function(key, element) {
        parent = $(element).parent().parent().prevAll().find("[name^='userprofile-0-user_occupation_']").last();

        if (parent.length && !parent.val()) {
            $(element).attr('disabled', 'disabled');
        }
    });
});
