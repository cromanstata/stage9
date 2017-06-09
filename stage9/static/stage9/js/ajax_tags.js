/**
 * Created by Admin on 5/9/2017.
 */
$(function () {
    console.log("trying to load tags function");
    //var loaded_tags = false;
    var loaded_tags_side = false;
    var assgined_for_sidebar = [];
    var titles_sidebar = [];
    //loads the ingridents allowed
    var ingredients_allowed = function (request) {
        var tmp = null;
        console.log("trying to load ingredients allowed V1");
        //if(loaded_tags) return;
        $.ajax({
            'async': false,
            'type': "GET",
            'dataType': "json",
            'url': "/diff_tags/",
            'data': {
                       term:request
                    },
            'success': function (data) {
                tmp = data;
                //console.log(tmp);
            }
        });
        //loaded_tags = true;
        return tmp;
    };
    //list of --all-- availble ingredients
    var all_ingrident_tags = getFields(ingredients_allowed('all'), "ingredient");

    //$(".ingredients_choices").innerHTML(all_ingrident_tags);
    
    //puts the ingredients aloowedn in side bar
    var sidetagsUpdate = function() {
        var tmp = null;
        console.log("trying to load side tags V1");
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
    };

    if ($('#ingredients_choices.way_of_search_class').length > 0) {
        sidetagsUpdate();
    }
/*
    $(window).on( "load", function() {
        var tmp = null;
        console.log("trying to load side tags V1");
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
    });

*/
    $('.myTags').tagit({
        //availableTags: all_ingrident_tags,
        allowSpaces: true,
        autocomplete: {
            source: function (request, response) {
                var that = this;
                $.ajax({
                    url: "/tags/",
                    dataType: "json",
                    data: {
                        term:request.term
                    },
                    success: function (choices){
                        var choices_names = getFields(choices, "ingredient");
                        console.log("from tagit",that.assignedTags());
                        if (anyMatchInArray(that.assignedTags(),choices_names)) {
                            var new_choices = that._subtractArray(choices_names, that.assignedTags());
                            choices = $.grep(choices, function (item) {
                                return new_choices.indexOf(item.ingredient) > -1;
                            });
                        }
                        response(
                            $.map(choices, function (item) {
                                return {
                                    label: item.slug,
                                    value: item.ingredient
                                };
                            }));
                    }
                });
            }
        },

        beforeTagAdded: function(event, tag) {
            if(all_ingrident_tags.indexOf(tag.tagLabel) == -1)
            {
                return false;
            }
        },

        afterTagAdded: function(event, tag) {
            assgined_for_sidebar = $('.myTags').tagit("assignedTags");
            var tag_slug = getFields(ingredients_allowed($('.myTags').tagit('tagLabel', tag.tag)), "slug");
            $('#chosen_for_typin_cont').append(
                $('<div/>')
                .attr("id", "sidebar-tag-" + tag_slug)
                .addClass("sidebar_selected_ingredients")
                .append(
                    $('<span/>')
                    .text($('.myTags').tagit('tagLabel', tag.tag))
                    .addClass("sidebar_selected_ingredients_text"),
                    $('<div/>')
                    .addClass("sidebar_selected_ingredients_delete")
                    .append(
                        $('<span/>')
                            .addClass("glyphicon glyphicon-trash icon-trash-side")
                    )
                )
            );
            var value_typin = $("#typin_tags").val();
            if (value_typin.length > 0 ) {
                $("#typin_tags").val("")
            }
        },

        afterTagRemoved : function(event, tag) {
            assgined_for_sidebar = $('.myTags').tagit("assignedTags");
            var tag_slug = getFields(ingredients_allowed($('.myTags').tagit('tagLabel', tag.tag)), "slug");
            $('#sidebar-tag-'+ tag_slug).remove();
        }
    });

    //STUFF FOR SIDEBAR BY SEARCH
    //auto complete and ENTER bind and select for search by title

    $( "#search_title_side").autocomplete({
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
    
    //autocomplete for typin tags in the side bar in home.html
    $( "#typin_tags").autocomplete({
        source: function (request, response) {
                var that = this;
                $.ajax({
                    url: "/tags/",
                    dataType: "json",
                    data: {
                        term:request.term
                    },
                    success: function (choices){
                        var choices_names = getFields(choices, "ingredient");
                        var assignedintagit = assgined_for_sidebar;
                        console.log("from side bar",assignedintagit);
                        if (anyMatchInArray(assignedintagit,choices_names)) {
                            var new_choices = choices_names.filter( function( el ) {
                              return assignedintagit.indexOf( el ) < 0;
                            } );
                            choices = $.grep(choices, function (item) {
                                return new_choices.indexOf(item.ingredient) > -1;
                            });
                        }
                        response(
                            $.map(choices, function (item) {
                                return {
                                    label: item.ingredient,
                                    value: item.ingredient
                                };
                            }));
                    }
                });
            },
        select: function(event, ui) {
                    var inp = (ui.item.value);
                    $('.myTags').tagit('createTag', inp);
                    $(this).val("");
                    return false;
                }
    });

    $("#typin_tags").keyup(function(e){
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    $("#typin_tags").bind("enterKey",function(e){
    //do stuff here
        var inp = ($("#typin_tags").val());
        $('.myTags').tagit('createTag', inp);
        //if (anyMatchInArray(all_ingrident_tags,$("#typin_tags").val())){
        //    alert ($("#typin_tags").val());
        //}
    });

    $(document).on('click', '.sidebar_selected_ingredients_delete',function(e){
        var inp = $(this).parent().children('.sidebar_selected_ingredients_text').text();
        $('.myTags').tagit('removeTagByLabel', inp);
    });
    
    //clear all button
    $("#clear_all").on("click", function (event) {
        event.preventDefault();
        $('#search_diff').val('');
        $('#search_cuisine').val('');
        $('#search_mealtype').val('');
        $('.myTags').tagit('removeAll');return false;
    })
});

