/**
 * Created by Admin on 5/13/2017.
 */
$(function () {
    
    $(document).on('submit','#unfollow', function(e){
        var profile_view = $("#unfollow").find('input[name="profile_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/follow/",
            'type': "GET",
            'data': {
                profile_view: profile_view,
                action: "unfollow"
            },
            'success': function() {
                $("#follow").show();
                $("#unfollow").hide();
            }
        });
    });

    $(document).on('submit','#follow', function(e){
        var profile_view = $("#follow").find('input[name="profile_view"]').val();
        e.preventDefault();
        $.ajax({
            'url':"/follow/",
            'type': "GET",
            'data': {
                profile_view: profile_view,
                action: 'follow'
            },
            'success': function(){
                $("#follow").hide();
                $("#unfollow").show();
            }
        });
    });
});