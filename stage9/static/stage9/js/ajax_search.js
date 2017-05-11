/**
 * Created by Admin on 5/6/2017.
 */
$(function () {

    var searchUpdate = function() {
            $.ajax({
                type: "POST",
                url: "/search/",
                data: {
                    'search_text': $('#search_ingredient').val(),
                    'search_cuisine': $('#search_cuisine').val(),
                    'search_mealtype': $('#search_mealtype').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                dataType: 'html',
                success: function searchSuccess(data, textStatus, jqXHR) {
                            $('#search-results').html(data);
                        }
            });
        };

    $('#search_ingredient').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#search_cuisine').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#search_mealtype').on("keyup",searchUpdate)
    .on("change", searchUpdate);
});

/**
$(function () {
    $('#search').keyup(function () {
        $.ajax({
            type: "POST",
            url: "/search/",
            data: {
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'html',
            success: function searchSuccess(data, textStatus, jqXHR) {
                        $('#search-results').html(data);
                    }
        });
    });
});


//function searchSuccess(data, textStatus, jqXHR) {
//    $('#search-results').html(data);
//}
 */
