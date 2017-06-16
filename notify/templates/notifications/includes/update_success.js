var updateSuccess = function (response) {
    var notification_box = $(nfBoxListClassSelector);
    var notifications = response.notifications;
    var $nf_count_badge = $('#notification_counter_badge');
    var current_count = parseInt($nf_count_badge.html());
    var to_be_added = parseInt(response.retrieved);
    $nf_count_badge.html(to_be_added + current_count);
    if ((current_count+to_be_added)==0) {
        $nf_count_badge.hide();
    }
    else {
       $nf_count_badge.show(); 
    }
    $.each(notifications, function (i, notification) {
        notification_box.prepend(notification.html);
    });
};
