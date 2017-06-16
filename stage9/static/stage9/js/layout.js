$(function () {
        // Get the modal
    var modal = document.getElementById('dynamic_modal');

    // Get the <span> element that closes the modal
    //var span = document.getElementsByClassName("close");

    $(document).on('click', '.allauth-link',function(e){
        modal.style.display = "block";
        var data = $(this).attr('datatype');
        allauthhUpdate(data);
    });
    // When the user clicks on <span> (x), close the modal
    //span.onclick = function() {
    //    modal.style.display = "none";
    //};

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
    
    var allauthhUpdate = function(allauth_data) {
        $.ajax({
            type: "GET",
            url: "/allauthpop/",
            dataType: 'html',
            data: {
                'allauth_data': allauth_data
            },
            success: function searchSuccess(data, textStatus, jqXHR) {
                        $('#allauthpop').html(data);
                    }
        });
    };

    var sideBar = document.getElementById('side_navbar');


    $(document).on('click', '#side_navbar_btn',function(e){
        sideBar.style.display = "none";
        $('#side_navbar_btn_hidden').show();
    });

    $(document).on('click', '#side_navbar_btn_hidden',function(e){
        $('#side_navbar_btn_hidden').hide();
        sideBar.style.display = "block";
    });

    $(document).on('click', '#top_bar_notifications',function(e){
        e.stopPropagation();
        $('#notification_box').toggle();
        $('.notification_box_arrow').toggle();
        //comment_more_menu_arrow
    });

    /*
    var hideSideBar = function () {
        $('#side_navbar').css({"width": "0"});
    };
    document.getElementById('side_navbar_meanu_icon').on('click', hideSideBar());
    */
});





