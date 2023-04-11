/** 聊天页面 websocket */
let ws = new WebSocket($("input[name='ws-connect']").attr("data-url"));

// 成功建立连接时获取默认会话的数据
ws.onopen = getHistories;
// 连接出错提示
ws.onerror = function () {
    alertBox();
}
// 接收服务端消息处理
ws.onmessage = getResponse;

// 接收服务器响应
function getResponse(response) {
    let $chatContent = $("#chatContent");
    let $handle = $("#handle");
    // 序列化response
    let data = JSON.parse(response.data);

    // 显示bot消息
    let botMessage = messageTemplate({
        sender: "bot",
        text: data.content,
        sendTime: data.timeStamp,
    });
    $(`${botMessage}`).insertBefore($handle);
    $handle.hide();

    // 滚动到底部
    $chatContent.animate({scrollTop: $chatContent[0].scrollHeight}, 250);

    // 启用发送按钮
    $("#sendMessage").prop('disabled', false);
}

// 发送用户对话
function sendUserMessage() {
    if (ws.readyState === ws.OPEN) {
        let $chatContent = $("#chatContent");
        let $handle = $("#handle");
        let $messageInput = $("#message")

        // 将用户信息显示在对话框中
        if ($messageInput.val() !== "") {
            // 禁用发送按钮
            $("#sendMessage").prop('disabled', true);

            // 渲染对话框模板
            let userMessage = messageTemplate({
                sender: "user",
                text: $messageInput.val(),
                sendTime: new Date().toLocaleString("zh-CN", {hour12: false})
            });
            $(`${userMessage}`).insertBefore($handle);
            $handle.show();

            // 发送消息
            ws.send($messageInput.val());
            // 清空输入框
            $messageInput.val("");

            // 滚动到底部
            $chatContent.animate({scrollTop: $chatContent[0].scrollHeight}, 250);
        }
    } else {
        alertBox({status: "error", message: "连接已关闭，请刷新页面重试"});
    }
}

// 响应回车键发送消息
$('#sendInput').on('keyup', function (e) {
    let $sendMessage = $("#sendMessage");
    e.preventDefault();
    if (e.key === "Enter" && !$sendMessage.prop('disabled')) {
        sendUserMessage();
    }
});


// 获取历史消息
function getHistories() {
    let $chatContent = $("#chatContent");
    alertBox({status: "success", message: "正在加载会话数据"});

    $.get(
        $chatContent.attr("data-url"),
        {sessionId: $(".dropdown").find("[aria-current]").attr("data-id")},
        function (data) {
            if (data.status === "success") {
                let messages = JSON.parse(data.content);

                for (let i = messages.length - 1; i >= 0; i--) {
                    let template = messageTemplate({
                        sender: messages[i].sender,
                        text: messages[i].text,
                        sendTime: messages[i].sendTime
                    });
                    $(`${template}`).insertBefore($("#handle"));
                }

                // 显示内容
                $chatContent.find("[name='content']").show();
                $chatContent.find("[name='timestamp']").show();
                // 滚动到底部
                $chatContent.animate({scrollTop: $chatContent[0].scrollHeight}, 250);

            } else if (data.status === "reload") {
                alertBox({status: "success", message: "正在重载会话, 请稍等"});
                setInterval(() => {
                    window.location.reload();
                }, 1000);

            }
        }
    );
}

// 切换会话
$("a.dropdown-item").click(function () {
    // 关闭当前会话连接
    ws.close();

    // 清空消息列表
    $("#chatContent > div").remove();

    // 切换会话列表显示
    $(".dropdown").find("[aria-current]").removeAttr("aria-current").removeClass("active");
    $(this).addClass("active").attr("aria-current", true);
    $("#currentSession").text($(this).text());

    // 连接指定会话
    ws = new WebSocket($("input[name='ws-connect']").attr("data-url") + `${$(this).attr("data-id")}/`);
    ws.onopen = getHistories;
    ws.onerror = function () {
        alertBox();
    }
    ws.onmessage = getResponse;
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


/** 语音识别-录音 */
let recoder = null;
let isRecording = false;

// 生成音频ID
function getUniqueId() {
    const temp_url = URL.createObjectURL(new Blob());
    const id = temp_url.toString();
    URL.revokeObjectURL(temp_url);
    return id.substring(id.lastIndexOf("/") + 1);
}

// 开始录音
function recoderAudio() {
    // 请求录音权限
    recoder = Recorder({sampleRate: 16000, type: "wav"});
    recoder.open(() => {
        console.log('已授予录音权限');
        // 开始录音
        recoder.start();
    }, (error) => {
        console.log(error);
    });
}

// 停止录音
function recoderStop() {
    // 停止录音
    recoder.stop((blob) => {
        recoder.close();
        // 转换为FormData
        let formData = new FormData();
        let fileName = "recoder-" + getUniqueId() + ".wav";
        formData.append("fileName", fileName);
        formData.append('filePath', blob, fileName);

        // 显示处理进度
        $("#modalButtonGroup").hide();
        $("div[name='audioHandle']").show();

        // 上传文件
        uploadAudio(formData, $("#fileUpload").attr("target"));
    });
}

// 绑定录音按钮事件
$("#recoding").click(function (e) {
    e.preventDefault();
    // 检查是否已开始录音
    if (!isRecording) {
        $(this).text("• 正在录音")
        recoderAudio();
        isRecording = true
    } else {
        $(this).text("录音")
        recoderStop();
        isRecording = false
    }
});


/** 语音识别-上传文件 */
// 返回转换文本
function returnAudioText(data) {
    if (data.status === "success") {
        $("#sttModal").modal('hide');
        $("#message").val(data.text);

        // 恢复上传窗口内容
        $("div[name='audioHandle']").hide();
        $("#modalButtonGroup").show();
    } else {
        alert("转换文件失败！");
    }
}

// 上传录音文件
function uploadAudio(data, url) {
    $.ajax({
        type: "post",
        url: url,
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
            alert("上传文件失败！");
        },
    });
}

// 绑定label事件
$("#fileInput").change(function () {
    // 取出音频文件
    let file = $("#fileInput").get(0).files[0];
    // 添加到表单数据中
    let formData = new FormData();
    formData.append("fileName", file["name"]);
    formData.append("filePath", file);

    // 显示处理进度
    $("#modalButtonGroup").hide();
    $("div[name='audioHandle']").show();

    // ajax发送给后台
    uploadAudio(formData, $("#fileUpload").attr("target"));
});