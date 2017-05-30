/**
 * Created by Admin on 5/28/2017.
 */
$(function () {

    function changeValue(value) {
      document.getElementById('id_rating').value = value;
    }

    var activeItem;
    $('.star-ratings-rating-empty').on('mouseenter mouseleave click', function(event){
        event.stopPropagation();
        var li = this.classList[1].match(/\d+/)[0];
        var li_num = Number(li);
        if(event.type == 'click') {
            if(activeItem == 0) {
                for (i = 0; i < li_num+1; i++) {
                    $(".rate_"+i).css({"background-color": "yellow"});
                }
                for (i = 4; li_num < i; i--) {
                    $(".rate_"+i).css({"background-color": ""});
                }
                changeValue((li_num+1).toFixed(1));
            } else {
                activeItem = 0;
                changeValue((li_num+1).toFixed(1));
            }
        }
        else if(event.type == 'mouseenter') {
            if(activeItem != 0) {
                for (i = 0; i < li_num+1; i++) {
                    $(".rate_"+i).css({"background-color": "yellow"});
                }
            }
        } else if(event.type == 'mouseleave') {
            if(activeItem != 0) {
                for (i = 0; i < li_num+1; i++) {
                    $(".rate_"+i).css({"background-color": ""});
                }
            }
        }
    });
});