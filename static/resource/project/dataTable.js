/**
 * Created by yoon on 2017. 6. 4..
 */

$(document).ready(function () {
    var dataSet = [];

    $.ajax({
        type: 'GET',
        url: '/getTableDataList',
        success: function (data) {
            if(data.result == 'success'){
                dataSet = data.dataList;
            }
        }
    });
    $('#commerceTable').DataTable({
        data: dataSet,
        columns:[
            { title: "아이템" },
            { title: "가격" },
            { title: "타이머" },
            { title: "반경 거리" },
            { title: "커머스 타이틀" },
            { title: "구매율" },
            { title: "구매 평균 연령" },
            { title: "구매 남녀 비율" },
        ]
    });
});