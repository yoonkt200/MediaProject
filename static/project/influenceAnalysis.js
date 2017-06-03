/**
 * Created by yoon on 2017. 6. 4..
 */

$(document).ready(function () {
    $('.form_prediction').submit(function (e) {
        e.preventDefault();
        if ($('.priceInput').val() == "") alert("커머스의 가격을 입력해주세요.");
        else if ($(".timerSelect option:selected").val() == '0') alert("타이머를 설정해주세요.");
        else if ($(".distanceSelect option:selected").val() == '0') alert("커머스 반경을 설정해주세요.");
        else {
            $.ajax({
                type: 'POST',
                data: $(this).serialize(),
                url: '/analysis_influence_prediction',
                success: function (data) {
                    if (data.result == 'fail') alert('error!');
                    else {
                        $('.result').text(data.result);
                    }
                }
            })
        }
    });
});