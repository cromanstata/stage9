/**
 * Created by Admin on 5/9/2017.
 */
$(function () {
    console.log("trying to load tags function");
    var loaded_tags = false;
    var loaded_tags_side = false;
    //loads the ingridents allowed
    var ingredients_allowed = function (request) {
        var tmp = null;
        console.log("trying to load ingredients allowed");
        if(loaded_tags) return;
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
                console.log(tmp);
            }
        });
        loaded_tags = true;
        return tmp;
    };
    //list of --all-- availble ingredients
    var all_ingrident_tags = getFields(ingredients_allowed('all'), "ingredient");
    //$(".ingredients_choices").innerHTML(all_ingrident_tags);
    
    //puts the ingredients aloowedn in side bar
    $(window).on( "load", function() {
        var tmp = null;
        console.log("trying to load side tags");
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
                        if (anyMatchInArray(that.assignedTags(),choices_names)) {
                            var new_choices = that._subtractArray(choices_names, that.assignedTags());
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
            }
        },

        beforeTagAdded: function(event, tag) {
            if(all_ingrident_tags.indexOf(tag.tagLabel) == -1)
            {
                return false;
            }
        }


    });
});

