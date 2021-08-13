// 发送验证码倒计时60s
$(function() {
	var btn = $("#send");
	$(function() {
		btn.click(settime);
	})
	var countdown = 5;//倒计时总时间，为了演示效果，设为5秒，一般都是60s
	function settime() {
		if (countdown == 0) {
			btn.attr("disabled", false);
			btn.html("获取验证码");
			btn.removeClass("disabled");
			countdown = 5;
			return;
		} else {
			btn.addClass("disabled");
			btn.attr("disabled", true);
			btn.html("重新发送(" + countdown + ")");
			countdown--;
		}
		setTimeout(settime, 1000);
	}

})