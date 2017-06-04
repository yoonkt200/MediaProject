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
                    if (data.result == "fail"){
                        alert("죄송합니다. 현재는 제휴아이템을 추천할 데이터가 모자랍니다.");
                    } else{
                        $('.rule1').text(data.rule1);
                        $('.rule2').text(data.rule2);
                        $('.rule1_support').text(data.rule1_support);
                        $('.rule2_support').text(data.rule2_support);
                    }
                }
            })
        }
    });
});