/**
 * Created by yoon on 2017. 6. 4..
 */

$(document).ready(function () {
    $('.form_recommendation').submit(function (e) {
        e.preventDefault();
        if ($(".itemSelect option:selected").val() == '0') alert("아이템을 선택해주세요.");
        else {
            $.ajax({
                type: 'POST',
                data: $(this).serialize(),
                url: '/recommend_item_rules',
                success: function (data) {
                    $('.rule1').text(data.rule1);
                    $('.rule2').text(data.rule2);
                    $('.rule1_support').text(data.rule1_support);
                    $('.rule2_support').text(data.rule2_support);
                }
            })
        }
    });
});