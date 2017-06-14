/**
 * Created by yoon on 2017. 6. 3..
 */

$(document).ready(function () {
    $('.form_login').submit(function (e) {
        if ($('.userId').val() == "") alert("아이디를 입력해주세요.");
        else if ($('.password').val() == "") alert("비밀번호를 입력해주세요.");
        else {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                data: $(this).serialize(),
                url: '/login',
                success: function (data) {
                    if (data.result == 'fail') alert('이메일주소 또는 비밀번호가 올바르지 않습니다');
                    else {
                        alert("환영합니다 " + data.name + "님! " + data.name + "님의 커머스 카테고리는 [" + data.category + "] 입니다.");
                        window.location.href = "/main";
                    }
                }
            })
        }
    });
});