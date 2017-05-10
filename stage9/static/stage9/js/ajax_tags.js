/**
 * Created by Admin on 5/9/2017.
 */
$(function () {
    var ingredient_tags =[];

    $(".myTags").tagit({
        //availableTags: sampleTags,

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
        }
    });
});

