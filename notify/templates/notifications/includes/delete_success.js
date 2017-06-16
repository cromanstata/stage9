var deleteSuccess = function (response, notification) {
    //console.log(response);
    var $selected_notification = notification.closest(nfClassSelector);
    var $nf_count_badge = $('#notification_counter_badge');
    var current_count = parseInt($nf_count_badge.html());

    $nf_count_badge.html(current_count-1);
    if ((current_count-1)==0) {
        $nf_count_badge.hide();
    }
    else {
       $nf_count_badge.show();
    }
    $selected_notification.fadeOut(300, function () {
        $(this).remove()
    });
};