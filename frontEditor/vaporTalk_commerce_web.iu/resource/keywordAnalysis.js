/**
 * Created by yoon on 2017. 6. 4..
 */

$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/getKeyword',
        success: function (data) {
            if(data.result == 'success'){
                $('.titleKeyword1').text(data.titleKeyword[0]);
                $('.titleKeyword2').text(data.titleKeyword[1]);
                $('.titleKeyword3').text(data.titleKeyword[2]);
                $('.contentKeyword1').text(data.contentKeyword[0]);
                $('.contentKeyword2').text(data.contentKeyword[1]);
                $('.contentKeyword3').text(data.contentKeyword[2]);
            }
        }
    });
});