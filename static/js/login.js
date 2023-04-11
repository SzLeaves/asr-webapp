/** 切换重置密码界面 */
function forgetPassword(is_return) {
    let $forgetForm = $("#forget");
    let $loginForm = $("#login");
    if (is_return) {
        refreshCaptcha();
        $forgetForm.hide();
        $forgetForm[0].reset();
        $loginForm.show();
    } else {
        $loginForm.hide();
        $forgetForm.show();
    }
}

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

/** 用户登录逻辑 */
$("button[data-type='login']").click(function (e) {
    // 阻止form的默认行为
    e.preventDefault();
    $.ajax({
        type: "post",
        dataType: "json",
        data: $("#login").serialize(),
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            // 显示弹窗
            alertBox(data);
            // 验证成功时重定向至app页面
            if (data.status === "success") {
                setTimeout(function () {
                    window.location.replace($("button[data-type='login']").attr("target"));
                }, 1500);
            }
        },
        error: function () {
            alertBox();
        },
    });
});

/** 用户忘记密码逻辑 */
$("button[data-type='forget']").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "post",
        url: $("button[data-type='forget']").attr("target"),
        dataType: "json",
        data: {
            "email": $("#forget input[name='email']").val(),
            "captcha_0": $("#forget input[name='captcha_0']").val(),
            "captcha_1": $("#forget input[name='captcha-input']").val(),
        },
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            // 验证失败刷新验证码
            if (data.status === "error") {
                refreshCaptcha();
            }

            alertBox(data);
            // 验证成功时刷新页面
            if (data.status === "success") {
                setTimeout(function () {
                    window.location.reload();
                }, 2000);
            }
        },
        error: function () {
            alertBox();
        },
    });
});

/** 用户重置密码界面逻辑 */
$("button[data-type='reset']").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "post",
        dataType: "json",
        data: $("#reset").serialize(),
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            alertBox(data);
            // 重置成功时重定向至登录页
            if (data.status === "success") {
                setTimeout(function () {
                    window.location.replace(
                        $("button[data-type='reset']").attr("target")
                    );
                }, 2000);
            }
        },
        error: function () {
            alertBox();
        }
    });
});


/** 用户注册逻辑 */
$("button[data-type='register']").click(function (e) {
    // 登录界面跳转至注册界面
    e.preventDefault();
    window.location.replace($("button[data-type='register']").attr("target"));
});

$("button[data-type='confrim-register']").click(function (e) {
    // 注册界面表单提交
    e.preventDefault();
    $.ajax({
        type: "post",
        dataType: "json",
        data: {
            "email": $("#register input[name='email']").val(),
            "password_1": $("#register input[name='password_1']").val(),
            "password_2": $("#register input[name='password_2']").val(),
            "captcha_0": $("#register input[name='captcha_0']").val(),
            "captcha_1": $("#register input[name='captcha-input']").val(),
        },
        async: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader(
                "X-CSRFToken",
                $("input[name='csrfmiddlewaretoken']").attr("value"));
        },
        success: function (data) {
            // 验证失败刷新验证码
            if (data.status === "error") {
                refreshCaptcha();
            }
            alertBox(data);
            // 注册成功时重定向至登录页
            if (data.status === "success") {
                setTimeout(function () {
                    window.location.replace(
                        $("button[data-type='confrim-register']").attr("target")
                    );
                }, 2000);
            }
        },
        error: function () {
            alertBox();
        }
    });
});