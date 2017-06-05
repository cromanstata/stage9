/**
 * Created by Admin on 5/14/2017.
 */
$(function () {
    
    $(document).on('click','#favorite-dashboard', function(e){
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
                var count = parseInt($(".favorite_count").text());
                count=count+1;
                $(".favorite_count").text(count);
                $('#favorite-dashboard').removeClass('not_pressed_red_grey');
                $('#favorite-dashboard').addClass('pressed_red_grey');
                $('#favorite-dashboard').attr("title","Remove from favorites").tooltip('fixTitle').tooltip('show');
                $('#favorite-dashboard').prop('id', 'unfavorite-dashboard');
            }
        });
    });
    
    $(document).on('click','#unfavorite-dashboard', function(e){
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
                var count = parseInt($(".favorite_count").text());
                count=count-1;
                $(".favorite_count").text(count);
                $('#unfavorite-dashboard').removeClass('pressed_red_grey');
                $('#unfavorite-dashboard').addClass('not_pressed_red_grey');
                $('#unfavorite-dashboard').attr("title","Add to favorite recipes").tooltip('fixTitle').tooltip('show');
                $('#unfavorite-dashboard').prop('id', 'favorite-dashboard');
            }
        });
    });
    
    $(document).on('click','#like-dashboard', function(e){
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
                var count = parseInt($(".like_count").text());
                count=count+1;
                $(".like_count").text(count);
                $('#like-dashboard').removeClass('not_pressed_grey_blue');
                $('#like-dashboard').addClass('pressed_blue_grey');
                $('#like-dashboard').attr("title","Remove like").tooltip('fixTitle').tooltip('show');
                $('#like-dashboard').prop('id', 'unlike-dashboard');
            }
        });
    });

    $(document).on('click','#unlike-dashboard', function(e){
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
                var count = parseInt($(".like_count").text());
                count=count-1;
                $(".like_count").text(count);
                $('#unlike-dashboard').removeClass('pressed_blue_grey');
                $('#unlike-dashboard').addClass('not_pressed_grey_blue');
                $('#unlike-dashboard').attr("title","Like recipe").tooltip('fixTitle').tooltip('show');
                $('#unlike-dashboard').prop('id', 'like-dashboard');
            }
        });
    });
});