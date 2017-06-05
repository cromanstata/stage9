$(document).ready(function() {
    // ADD COMMENT //
    $('.add-comment-form').submit(function(event){
        event.preventDefault();
        var form = $(this);
        var data =  new FormData(form.get(0));
        $.ajax({
            url: $('.add-comment-form').attr('action'),
            type: "POST",
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(json) {
                if (json['success'] == 0) {
                  errors = ""
                  for (var err in json['error']){
                    errors += "" + err + ": " + json['error'][err] + "\n"
                  }
                  alert(errors)                      
                }
                else {
                    var comment_count = document.getElementById('comments-count');
                    var comment_text = json['html'];
                    console.log (comment_text);
                    if (parseInt(comment_count.innerHTML) == 0) {
                        comment_count.innerHTML = parseInt(comment_count.innerHTML) + 1 + " Comment";
                    } else {
                        comment_count.innerHTML = parseInt(comment_count.innerHTML) + 1 + " Comments";
                    }
                    html = "<div id='comment-div-" + json['id'] + "' class='comment'>"+json['html']+"</div>"
                	$('.comments').prepend(html);
                	$('textarea#id_comment').val(" ");
                    if ($('#id_rating').val()>0) {
                        $('#rate_the_recipe').hide()
                    }
                    $('#no-comments').hide()
                }

            },
            error: function(response) {
            	alert("error")
            }
         });        
    });
    
    // DELETE COMMENT //
    $('.comments-wrapper').on('click', '.comment-delete-class', function(event) {
        event.preventDefault();
        var id = $(this).attr('data-id');
        if(confirm("Are you sure you want to delete this comment?")){
              $.ajax({
              type: "GET",
              url: $('.comment-delete-form').attr('action'),
              data: {'id': id, 'csrfmiddlewaretoken' : $("#csrf").attr('value')},
              success: function(data){
                    if(data['success'] == 1) {
                          $('#comment-div-' + id).remove()
                          if (data['count'] == 0) {
                                $('#no-comments').show()
                          }
                          else {
                                var comment_count = document.getElementById('comments-count');
                                if (data['count'] == 1) {
                                    comment_count.innerHTML = parseInt(comment_count.innerHTML) - 1 + " Comment";
                                } else {
                                    comment_count.innerHTML = parseInt(comment_count.innerHTML) - 1 + " Comments";
                                }
                                $('#no-comments').hide()
                          }
                    }
                    else {
                          alert("You don't have permission to delete this comment")
                    }
              }
          });
        }
    });

        // THREE DOTS MENU POP //
    $('.comments-wrapper').on('click', '.comment_more', function(event){
        event.stopPropagation();
        var id = $(this).attr('data-id');
        $('#comment-more-arrow-' + id).toggle();
        $('#comment-more-' + id).toggle();
    });

    $(".comment_more_menu_arrow").on("click", function (event) {
        event.stopPropagation();
    });

    $(".ccomment_more_menu").on("click", function (event) {
        event.stopPropagation();
    });

        // COMMENT EDIT //

    $('.comments-wrapper').on('click', '.comment-edit-class', function(event){
        var id = $(this).attr('data-id');
        $('#comment-edit-' + id).show();
        $('#comment-' + id).hide();
        $('#comment-likes-' + id).hide();
    });

    $('.comments-wrapper').on('submit', '.edit-form', function(event){
    event.preventDefault();
    var form = $(this);
    var data = form.serialize();
    var id = $(this).attr('data-id');
    var comment = document.getElementById('comment-'+id);
    var error = document.getElementById('edit-form-errors');
    $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: data,

            success: function(data){
                json = JSON.parse(data);
                if(json.success == 1) {
                    comment.innerHTML = $('#input-comment-' + id).val();
                    $('#comment-edit-' + id).hide();
                    $('#comment-' + id).show();
                } else if(json.success == 0){
                    console.log("FALUERE");
                     errors = ""
                  for (var err in json.error){
                    errors += "" + json.error[err] + "\n";
                }
                error.innerHTML = errors;
            }
                $('#comment-likes-' + id).show();
            },
            dataType: 'html'
        });
    });


    // LIKE UNLIKE COMMENT //
    $('.comments-wrapper').on('click', '.like-comment-btn', function() {
        var id = $(this).attr('data-id');
        if($(this).attr('data-like') == 'like') {
            $.ajax({
                type: "GET",
                url: '/comments/like',
                data: {'comment_id': id},
                success: function(data){
                    if(data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'liked');
                        $('#like-btn-' + id).removeClass('not_pressed_grey');
                        $('#like-btn-' + id).addClass('pressed_blue');
                        console.log (data['likes_count']);
                        $('#likes-count-' + id).text(data['likes_count']);
                    } else{
                        alert(data['error']);
                    }
                }
            });
        } else {
            $.ajax({
                type: "GET",
                url: '/comments/unlike',
                data: {'comment_id': id},
                success: function(data){
                    if(data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'like');
                        $('#like-btn-' + id).removeClass('pressed_blue');
                        $('#like-btn-' + id).addClass('not_pressed_grey');
                        $('#likes-count-' + id).text(data['likes_count']);
                    } else{
                        alert(data['error']);
                    }
                }
            });
        }
    });

})