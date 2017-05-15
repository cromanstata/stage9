/**
 * Created by Admin on 5/14/2017.
 */
$(function () {
    
    $(document).on('submit','#favorite', function(e){
        var recipe_view = $("#favorite").find('input[name="recipe_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/recipes/favorite/",
            'type': "GET",
            'data': {
                recipe_view: recipe_view,
                action: "favorite"
            },
            'success': function() {
                $("#unfavor").show();
                $("#favorite").hide();
            }
        });
    });
    
    $(document).on('submit','#unfavor', function(e){
        var recipe_view = $("#unfavor").find('input[name="recipe_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/recipes/favorite/",
            'type': "GET",
            'data': {
                recipe_view: recipe_view,
                action: 'unfavor'
            },
            'success': function(){
                $("#unfavor").hide();
                $("#favorite").show();
            }
        });
    });
    
    $(document).on('submit','#like_recipe', function(e){
        var recipe_view = $("#like_recipe").find('input[name="recipe_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/recipes/like/",
            'type': "GET",
            'data': {
                recipe_view: recipe_view,
                action: "like"
            },
            'success': function() {
                $("#unlike_recipe").show();
                $("#like_recipe").hide();
                var count = parseInt($(".like_count").text());
                count=count+1;
                $(".like_count").html(count);
            }
        });
    });

    $(document).on('submit','#unlike_recipe', function(e){
        var recipe_view = $("#unlike_recipe").find('input[name="recipe_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/recipes/like/",
            'type': "GET",
            'data': {
                recipe_view: recipe_view,
                action: "unlike"
            },
            'success': function() {
                $("#like_recipe").show();
                $("#unlike_recipe").hide();
                var count = parseInt($(".like_count").text());
                count=count-1;
                $(".like_count").html(count);
            }
        });
    });
});