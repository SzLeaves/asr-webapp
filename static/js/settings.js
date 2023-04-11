/** 刷新验证码 */
function refreshCaptcha() {
    $.getJSON("/captcha/refresh/", function (result) {
        $("img[class='captcha']").attr("src", result["image_url"]);
        $("#id_captcha_0").val(result["key"]);
    });
}

/** 提示弹窗 */
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

$("img[class='captcha']").click(function () {
    refreshCaptcha();
});

/** 重置密码 */
$("#reset").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "post",
        dataType: "json",
        data: {
            "password_1": $("input[id='password_1']").val(),
            "password_2": $("input[id='password_2']").val(),
            "captcha_0": $("input[name='captcha_0']").val(),
            "captcha_1": $("input[id='captcha-input']").val(),
        },
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            alertBox(data);
            if (data.status === "success") {
                // 重定向至登录页面
                setTimeout(function () {
                    window.location.replace(
                        $("button[id='reset']").attr("target")
                    );
                }, 2000);
            } else {
                // 刷新验证码
                refreshCaptcha();
            }
        },
        error: function () {
            alertBox();
        }
    });
});


/** 删除转换记录 */
$("a[data-id]").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "post",
        url: $("#transHistories").attr("data-url"),
        dataType: "json",
        data: {"id": $(this).attr("data-id")},
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            // 删除表格记录
            $(`a[data-id=${data.id}]`).closest("tr").remove();
            alertBox(data);
        },
        error: function () {
            alertBox();
        }
    });
});


/** 修改会话操作 */

let $sessionModal = $("#sessionModal");
const sessionModal = new bootstrap.Modal($sessionModal);
$sessionModal.on('hide.bs.modal', function (e) {
    $("#sessionGroup").find("input").val("");
    $("#sessionGroup > div").hide();
    $(".modal-footer").show();
})

/* 显示模态框 */

// 添加会话
$("#addSession").click(function (e) {
    e.preventDefault();
    let $adds = $("#adds");

    $("#sessionModal h5").text($adds.attr("title"))
    $adds.show();
    sessionModal.show();
});

// 修改会话
let editId = null;
$("img[data-type='edit']").click(function (e) {
    e.preventDefault();
    let $edit = $("#edit");
    editId = $(this).parent().attr("data-id");

    $("#sessionModal h5").text($edit.attr("title"))
    $edit.show();
    sessionModal.show();
});

// 删除会话
let deleteId = null;
$("img[data-type='remove']").click(function (e) {
    e.preventDefault();
    let $remove = $("#remove");
    deleteId = $(this).parent().attr("data-id");

    $("#sessionModal h5").text($remove.attr("title"))
    $(".modal-footer").hide(); // 隐藏footer
    $remove.show();
    sessionModal.show();
});

/* 模态框操作 */

// 新增/修改会话
$("button[data-type='save-btn']").click(function (e) {
    e.preventDefault();

    let $newInput = $("input[name='new-input']");
    let $editInput = $("input[name='edit-input']");

    if ($newInput.val() !== "") {
        // 新增操作
        $.ajax({
            type: "post",
            url: $("#adds").attr("data-url"),
            dataType: "json",
            data: {sessionName: $newInput.val()},
            async: true,
            beforeSend: function (xhr) {
                xhr.setRequestHeader(
                    "X-CSRFToken",
                    $("input[name='csrfmiddlewaretoken']").attr("value"));
            },
            success: function (data) {
                alertBox(data);
                // 添加新记录
                if (data.status === "success") {
                    let record = recordTemplate({
                        id: data.id,
                        name: data.name,
                        startTime: data.startTime,
                    });
                    $("#sessionHistories").append(record);
                }
            },
            error: function () {
                alertBox();
            },
        });

    } else if ($editInput.val() !== "" && editId !== null) {
        // 修改操作
        $.ajax({
            type: "post",
            url: $("#edit").attr("data-url"),
            dataType: "json",
            data: {
                sessionId: editId,
                sessionName: $editInput.val()
            },
            async: true,
            beforeSend: function (xhr) {
                xhr.setRequestHeader(
                    "X-CSRFToken",
                    $("input[name='csrfmiddlewaretoken']").attr("value"));
            },
            success: function (data) {
                alertBox(data);
                // 修改会话名称
                if (data.status === "success") {
                    $(`tr[data-id='${data.id}'] td:first`).text(data.name);
                    editId = null;
                }
            },
            error: function () {
                alertBox();
            },
        });
    }

    sessionModal.hide();
});

// 删除会话
$("button[data-type='delete-btn']").click(function (e) {
    e.preventDefault();

    $.ajax({
        type: "post",
        url: $("#remove").attr("data-url"),
        dataType: "json",
        data: {sessionId: deleteId},
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            alertBox(data);
            // 移除被删除的记录
            if (data.status === "success") {
                $(`tr[data-id='${deleteId}']`).remove();
                deleteId = null;
            }
        },
        error: function () {
            alertBox();
        },
    });

    sessionModal.hide();
});