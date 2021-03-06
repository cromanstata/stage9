/**
 * Created by Admin on 6/18/2017.
 */
$(function () {
    var titles_sidebar = [];
    //var loaded_tags_side = false;
    //auto complete for titles
    $( "#search_author_side_title").autocomplete({
        source: function (request, response) {
                var that = this;
                $.ajax({
                    url: "/titles/",
                    dataType: "json",
                    data: {
                        term:request.term
                        //search_list: search_list_ajax
                    },
                    success: function (choices){
                        var choices_names = getFields(choices, "title");
                        var assignedintitles = titles_sidebar;
                        //filter just the titles that already show in the results
                        if (anyMatchInArray(assignedintitles,choices_names)) {
                            var new_choices = choices_names.filter( function( el ) {
                              return assignedintitles.indexOf( el ) < 0;
                            } );
                            choices = $.grep(choices, function (item) {
                                return new_choices.indexOf(item.title) > -1;
                            });
                        }
                        response(
                            $.map(choices, function (item) {
                                return {
                                    label: item.title,
                                    value: item.title
                                };
                            }));
                    }
                });
            },
        minLength: 2
    });
    
    //funtion that updates the search according to filters tags or title
    var authorUpdate = function() {
            $.ajax({
                type: "POST",
                url: "/authorsearch/",
                data: {
                    'search_title': $('#search_author_side_title').val(),
                    'search_cuisine': $('#search_author_side_cuisine').val(),
                    'search_mealtype': $('#search_author_side_mealtype').val(),
                    'search_difficulty': $('#search_author_side_difficulty').val(),
                    'author': $('#search_author_side_author').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                dataType: 'html',
                success: function searchSuccess(data, textStatus, jqXHR) {
                            $('#search-results-author').html(data);
                        }
            });
        };

    if ($('#search-results-author.search_results_has_api').length > 0)
    {
        $('#search_author_side_title').val('');
        $('#search_author_side_cuisine').val('');
        $('#search_author_side_mealtype').val('');
        $('#search_author_side_difficulty').val('');
        $('.author_navbar_item').css({
            'background-color': 'white',
            'color': 'black'
        });
        authorUpdate();
    }
    
    $('#author_unmark_all').on("click", function() {
        $('#search_author_side_title').val('');
        $('#search_author_side_cuisine').val('');
        $('#search_author_side_mealtype').val('');
        $('#search_author_side_difficulty').val('');
        $('.author_navbar_item').css({
            'background-color': 'white',
            'color': 'black'    
        });
    });
    
    $('.author_navbar_item').on("click", function() {
        var id = $(this).attr('data-id');
        var click = $(this).attr('data-like');
        var model = $(this).attr('data-model-name');
        console.log(model);
        if (click == "click") {
            $(this).css({
                'background-color': 'red',
                'color': 'white'
            });
            $(this).attr('data-like', 'clicked');
            if ($("#search_author_side_"+model).val() == '') {
                $("#search_author_side_"+model).val($("#search_author_side_"+model).val()+id);
            }
            else {
                $("#search_author_side_"+model).val($("#search_author_side_"+model).val()+","+id);
            }
        }
        else {
        $(this).css({
            'background-color': 'white',
            'color': 'black'
        });
        $(this).attr('data-like', 'click');

        var values = $("#search_author_side_"+model).val().split(",");
        var newValue = "";
        for ( var i = 0 ; i < values.length ; i++ )
        {
        if ( id != values[i] && "" != values[i] )
            {
                if (newValue.length == 0) {
                    newValue = values[i];
                }
                else {
                    newValue = newValue + "," + values[i];
                }
            }
        }
        $("#search_author_side_"+model).val( newValue );
        }
        authorUpdate();
    });
    
    $('#author_unmark_all').on("click",authorUpdate);

    $("#search_author_side_title").keyup(function(e){
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
        if (e.keyCode==8)
        {
            $(this).trigger("backSpace");
        }
    });
    $("#search_author_side_title").bind("enterKey",authorUpdate);
    $("#search_author_side_title").bind("backSpace",function (){
        //if (!this.value && ((('#search_mealtype').value) || ((('#search_cuisine').value) || ((('#search_diff').value) || ('#search_mealtype').value)))) {
        if (!this.value) {
            //&& (($('#search_mealtype').val()!=null))) {
        //    console.log($('#search_mealtype').val());
        //    alert ("reload if there are search values");
            authorUpdate();
        }
    });
    $("#search_author_side_title").on( "autocompleteselect", function(event, ui) {
        var inp = (ui.item.value);
        $("#search_author_side_title" ).val(inp);
        authorUpdate();
        return true;
    });
});/**
 * Created by Admin on 6/19/2017.
 */
