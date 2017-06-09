/**
 * Created by Admin on 5/6/2017.
 * 
 * 
 */
$(function () {
    //var loaded_tags_side = false;
    
    //funtion that updates the search according to filters tags or title
    var searchUpdate = function() {
            $.ajax({
                type: "POST",
                url: "/search/",
                data: {
                    'search_text': $('#search_ingredient').val(),
                    'search_cuisine': $('#search_cuisine').val(),
                    'search_mealtype': $('#search_mealtype').val(),
                    'search_title': $('#search_title_side').val(),
                    'search_diff': $('#search_diff').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                dataType: 'html',
                success: function searchSuccess(data, textStatus, jqXHR) {
                            $('#search-results').html(data);
                        }
            });
        };
    
    if ($('#search-results.search_results_has_api').length > 0)
    {
        searchUpdate();
    }
    
    $('#search_ingredient').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#search_diff').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#search_cuisine').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#search_mealtype').on("keyup",searchUpdate)
    .on("change", searchUpdate);
    $('#clear_all').on("click",searchUpdate);
    $("#search_title_side").keyup(function(e){
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
        if (e.keyCode==8)
        {
            $(this).trigger("backSpace");
        }
    });
    $("#search_title_side").bind("enterKey",searchUpdate);
    $("#search_title_side").bind("backSpace",function (){
        //if (!this.value && ((('#search_mealtype').value) || ((('#search_cuisine').value) || ((('#search_diff').value) || ('#search_mealtype').value)))) {
        if (!this.value) {
            //&& (($('#search_mealtype').val()!=null))) {
        //    console.log($('#search_mealtype').val());
        //    alert ("reload if there are search values");
            searchUpdate();
        }
    });
    $("#search_title_side").on( "autocompleteselect", function(event, ui) {
        var inp = (ui.item.value);
        $("#search_title_side" ).val(inp);
        searchUpdate();
        return true;
    });
    //$( "#search_title_side:empty" ).on("change",searchUpdate);

/*
    function searchTagsVisible(){
        var tmp = null;
        console.log("trying to load side tags V2");
        if(loaded_tags_side) return;
        $.ajax({
         type: "GET",
            url: "/availble_tags/",
            dataType: 'html',
            success: function searchSuccess(data, textStatus, jqXHR) {
                        $('#ingredients_choices').html(data);
                        loaded_tags_side = true;
                    }
        });
    }
    
    */

    //$('#ingredients_choices').bind('searchTagsVisible', searchTagsVisible);
    
    $('.way_of_search_item').on("click", function (event) {
        event.stopPropagation();
        if($(this).attr('id') == 'way_of_search_click') {
            $('#ingredients_choices').show(
                //function () {
                //    $(this).trigger('searchTagsVisible')
                //}
            );
            $('#ingredients_typein').hide();
            $('#ingredients_forlazy').hide();
        }
        if($(this).attr('id') == 'way_of_search_key') {
            $('#ingredients_typein').show();
            $('#ingredients_forlazy').hide();
            $('#ingredients_choices').hide();
        }
        if($(this).attr('id') == 'way_of_search_lazy') {
            $('#ingredients_forlazy').show();
            $('#ingredients_typein').hide();
            $('#ingredients_choices').hide();
        }
    });

        /*
        //showing the search results in the div#search_results
    $('#search_results_ajax').on("load", function (event) {
       document.getElementById("search_results").style.display = "block";
    });
    */
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
