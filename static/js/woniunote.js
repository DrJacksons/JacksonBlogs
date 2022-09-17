//显示模态框中的登录面板
function showLogin() {
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $("#mymodal").modal('show');
}
//显示模态框中的注册面板
function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $("#mymodal").modal('show');
}

//发送邮件功能
function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    // 对邮箱地址进行校验（xxx@xxx.xx）
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确。"});
        $("#regname").focus();
        return false;
    }
    $.post('/ecode', 'email='+email, function (data) {
        if (data == "email-invalid") {
            bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确。"});
            $("#regname").focus();
            return false;
        }
        else if (data == "send-pass") {
            bootbox.alert({title:"信息提示", message:"邮箱验证码已成功发送，请查收。"});
            $("#regname").attr('disabled', true);  //验证码发送完成后禁止修改注册邮箱
            $(obj).attr('disabled', true);  //发送邮件按钮变为不可用
            return false;
        }
        else {
            bootbox.alert({title:"错误提示", message:"邮箱验证码未发送成功。"});
            return false;
        }
    })
}

//用户注册按钮
function doReg() {
    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());
    console.log(regcode);

    if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {
        bootbox.alert({title:"错误提示", message:"注册的邮箱不正确或者密码少于5位"});
        return false
    }
    else {
        // 构建POST请求的正文数据
        var param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        // 利用JQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/reg', param, function (data) {
            if (data == "ecode-error") {
                bootbox.alert({title:"错误提示", message:"验证码无效。"});
                $("#regcode").val('');  // 清除验证框的数据
                $("#regcode").focus();
            }
            else if (data == "up-invalid") {
                bootbox.alert({title:"错误提示", message:"用户名和密码不能少于5位数。"});
            }
            else if (data == "user-repeated") {
                bootbox.alert({title:"错误提示", message:"该用户已经被注册。"});
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                bootbox.alert({title:"信息提示", message:"恭喜你，注册成功。"});
                // 注册成功后，延迟1秒重新刷新当前页面即可
                setTimeout('location.reload();', 1000);
            }
            else if (data == "reg-fail") {
                bootbox.alert({title:"错误提示", message:"注册失败，请联系管理员。"});
            }
        });
    }
}

// 用户登录按钮
function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());
    if (loginname.length < 5 || loginpass.length < 5) {
        bootbox.alert({title:"错误提示", message:"用户名和密码少于5位"});
        return false;
    }
    else {
        //构建POST请求的正文数据
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        // 利用JQuery框架发送POST请求，并获取到后台登录接口的响应内容
        $.post('/login', param, function (data) {
            if (data == "vcode-error") {
                bootbox.alert({title:"错误提示", message:"验证码无效。"});
                $("#logincode").val('');
                $("#logincode").focus();
            }
            else if (data == "login-pass") {
                bootbox.alert({title:"信息提示", message:"恭喜你，登录成功。"});
                setTimeout('location.reload();', 1000);
            }
            else if (data == "login-fail") {
                bootbox.alert({title:"错误提示", message:"登录失败，请联系管理员。"});
            }

        });
    }
}

// 点击图片切换
function imgJump() {
    imge=document.getElementById("loginvcode");
	var time=new Date().getTime();
	imge.src="/vcode?time="+time;
}