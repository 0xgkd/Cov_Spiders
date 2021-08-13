function flush_time() {
	$.ajax({
		url:"/time",
		timeout: 5000, //超时时间设置为5s
		success: function (data) {
			$("#time").html(data)
		},
		error: function (xhr, type, errorThrown) {
			//alert("获取时间失败")
		}
	});
}

function get_c1_data() {
	$.ajax({
		url:"/c1",
		success: function (data) {
			$(".num h1").eq(0).text(data.confirm)
			$(".num h1").eq(1).text(data.heal)
			$(".num h1").eq(2).text(data.dead)
			$(".num h1").eq(3).text(data.nowConfirm)
		},
		error: function (xhr, type, errorThrown) {
			// 反馈错误信息
		}
	});
}

function get_c2_data() {
	$.ajax({
		url:"/c2",
		success: function(data) {
			optionMap.series[0].data = data.data
			ec_center.setOption(optionMap)
		},
		error: function(xhr, type, errorThrown) {
		
		}
	})
}

function get_l1_data() {
	$.ajax({
		url:"/l1",
		success: function(data) {
			option_left1.xAxis.data = data.dateID
			option_left1.series[0].data = data.confirmedCount
			option_left1.series[1].data = data.curedCount
			option_left1.series[2].data = data.deadCount
			option_left1.series[3].data = data.currentConfirmedCount
			ec_left1.setOption(option_left1)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}



function get_l2_data() {
	$.ajax({
		url:"/l2",
		success: function(data) {
			option_left2.xAxis.data = data.dateID
			option_left2.series[0].data = data.confirmedIncr
			option_left2.series[1].data = data.curedIncr
			ec_left2.setOption(option_left2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


function get_r1_data() {
	$.ajax({
		url:"/r1",
		success: function(data) {
			option_right1.xAxis.data = data.provinceName
			option_right1.series[0].data = data.currentConfirmedCount
			ec_right1.setOption(option_right1)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


function get_r2_data() {
	$.ajax({
		url:"/r2",
		success: function(data) {
			option_right2.series[0].data = data.kws
			ec_right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}

flush_time()
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()
setInterval(flush_time, 1000)
setInterval(get_c1_data, 1000*10)
setInterval(get_c2_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
