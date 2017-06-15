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
});





