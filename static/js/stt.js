/** 音频文件转文字 */

function returnAudioText(data) {
    if (data.status === "success") {
        alertBox({status: data.status, message: "转换成功"});
        $("#process").hide();
        $("#resultText p").text(data.text)
        $("#resultText").show();
    } else {
        alertBox({status: "error", message: "转换失败"});
    }
}

function uploadAudio(data) {
    $.ajax({
        type: "post",
        contentType: false,
        processData: false,
        async: true,
        data: data,
        dataType: "json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            returnAudioText(data);
        },
        error: function () {
            alertBox({status: "error", message: "上传文件失败"});
        },
    });
}

$("#fileInput").change(function () {
    // 取出音频文件
    let file = $("#fileInput").get(0).files[0];
    // 添加到表单数据中
    let formData = new FormData();
    formData.append("fileName", file["name"]);
    formData.append("filePath", file);

    // 显示文件及进度
    $("#fileUpload").hide();
    $("#uploaded")
        .css("display", "flex")
        .css("flex-direction", "column")
        .css("justify-content", "center")
        .css("align-items", "center");
    $("#uploaded strong").text("文件：" + file["name"]);

    // ajax发送给后台
    uploadAudio(formData);
});

/** 弹窗 */
function alertBox(data = null) {
    let $alertBox = $("#alert-box");
    let success = "alert-success";
    let danger = "alert-danger";

    if (data !== null) {
        if (data.status === "success") {
            // 表单验证成功文本提示
            $("#alert-box span").text(data.message);
            // 设置提示框样式
            if ($alertBox.hasClass(danger)) {
                $alertBox.removeClass(danger);
            }
            $alertBox.addClass(success);

        } else {
            $("#alert-box span").text(data.message);
            $alertBox.addClass("alert-danger");
        }
    } else {
        $("#alert-box span").text("unknow error");
        $alertBox.addClass("alert-danger");
    }

    // 弹窗显示动画效果
    $alertBox.fadeIn('slow').delay(1500).fadeOut('slow');
}
