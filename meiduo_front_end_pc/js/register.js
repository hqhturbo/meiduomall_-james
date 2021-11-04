var app = new Vue({
	el: '#app',
	data: {
		username: '',
		error_name: false,
		error_name_message: '',
		statu_name: '',
		host: host,
		statu_phone: '',
		mobile: '',
		error_phone: false,
		error_phone_message: '',
		password: '',
		error_password: false,
		password2: '',
		error_check_password: false,
		allow: false,
		error_allow: '',
		error: '',
		image_code: '',
		image_code_url: '',
		error_image_code: '',
		error_image_code_message: '',
		sms_code: '',
		check_sms_code: '',
		error_sms_code_message: '',
		error_sms_code: '',
		sms_code_tip: '点击获取验证码'
	},
	mounted: function() {
		this.generate_image_code()
	},
	methods: {
		generateUUID: function() {
			var d = new Date().getTime();
			if (window.performance && typeof window.performance.now === "function") {
				d += performance.now(); //use high-precision timer if available
			}
			var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
				var r = (d + Math.random() * 16) % 16 | 0;
				d = Math.floor(d / 16);
				return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
			});
			return uuid;
		},
		// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
		generate_image_code: function() {
			// 生成一个编号 : 严格一点的使用uuid保证编号唯一， 不是很严谨的情况下，也可以使用时间戳
			this.uuid = this.generateUUID();
			// 设置页面中图片验证码img标签的src属性
			this.image_code_url = this.host + "/image_codes/" + this.uuid + '/';
		},
		//发送短信验证码
		send_sms_code: function() {
			if (this.sending_flag == true) {
				return;
			}
			this.sending_flag = true;

			// 校验参数，保证输入框有数据填写
			this.check_phone();
			this.check_image_code();

			if (this.mobile_error == true || this.image_code_error == true) {
				this.sending_flag = false;
				return;
			}

			// 向后端接口发送请求，让后端发送短信验证码
			var url = this.host + '/sms_codes/?mobile=' + this.mobile + '&image_code=' + this.image_code +
				'&uuid=' + this.uuid;
			axios.get(url, {
					responseType: 'json'
				})
				.then(response => {
					console.error(response.data)
					// 表示后端发送短信成功
					if (response.data.code == 0) {
						
						// 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
						var num = 60;
						// 设置一个计时器
						var t = setInterval(() => {
							if (num == 1) {
								// 如果计时器到最后, 清除计时器对象
								clearInterval(t);
								// 将点击获取验证码的按钮展示的文本回复成原始文本
								this.sms_code_tip = '获取短信验证码';
								// 将点击按钮的onclick事件函数恢复回去
								this.sending_flag = false;
							} else {
								num -= 1;
								// 展示倒计时信息
								this.sms_code_tip = num + '秒';
							}
						}, 1000, 60)
					} else {
						if (response.data.code == '400') {
							//图片验证码错误
							this.image_code_error = true;
						}
						alert(response.data.errmsg)
						this.sms_code_error = true;
						this.generate_image_code();
						this.sending_flag = false;
					}
				})
				.catch(error => {
					console.log(error.response);
					this.sending_flag = false;
				})
		},
		check_username: function() {
			var that = this; //js闭包；js作用域范围问题
			var username = that.username //获取到了用户在文本框中输入的信息
			//http:127.0.0.1//
			axios.get(that.host + '/usernames/' + username + '/count/').then(function(resp) {
				console.log(resp)
				that.error_name_message = resp.data.errmsg
				if (resp.data.code == 200) {
					// that.error_name=false
					// that.statu_name='color:green'
				} else {
					that.error_name = true
					// that.error_name=true
					that.statu_name = 'color:red'
				}
			}).catch(function(err) {
				console.log(err)
			})
		},
		check_phone: function() {
			var that = this; //js闭包；js作用域范围问题
			var check_phone = that.mobile //获取到了用户在文本框中输入的信息
			var reg = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/;
			var r = reg.test(check_phone)
			if (!r) {
				that.error_phone = true
				that.error_phone_message = '手机号码格式不正确'
				return
			}

			axios.get(that.host + '/mobile/' + check_phone + '/count/').then(function(resp) {
				console.log(resp)
				that.error_phone_message = resp.data.errmsg
				if (resp.data.code == 200) {
					// that.error_name=false
					that.statu_phone = 'color:green'
					return true;
				} else {
					that.error_phone = true
					that.statu_phone = 'color:red'
					return false;
				}
			}).catch(function(err) {
				console.log(err)
			})
		},
		//检查验证码
		check_image_code: function() {
			if (!this.image_code) {
				this.image_code_error = true;
			} else {
				this.image_code_error = false;
			}
		},
		check_pwd: function() {
			var reg = /^[a-zA-Z]\w{5,17}$/;
			if (!reg.test(this.password)) {
				this.error_password = true
			} else {
				this.error_password = false
			}
		},
		check_cpwd: function() {
			if (this.password == this.password2) {
				this.error_check_password = false;
			} else {
				this.error_check_password = true;
			}
		},
		on_submit: function() {
			var that = this;
			//再次校验文本框中的值
			// debugger
			if (this.error_name || !this.allow || this.error_check_password || this.error_password || this
				.error_phone) {
				return this.prevent = false;
			}
			//发送ajax请求
			var url = this.host + '/register/';
			var data = {
				username: this.username,
				password: this.password,
				password2: this.password2,
				mobile: this.mobile
			}
			axios.post(url, data, {
				// responseType 表示服务器响应的数据类型，可以是 arraybuffer、blob、document、json、text、stream
				responseType: 'json', // default
				// withCredentials 表示跨域请求时是否需要使用凭证
				withCredentials: true, // default
			}).then(function(resp) {
				if (resp.data.code == 400) {
					that.error = resp.data.errmsg
				} else if (resp.data.code == 200) {
					window.location.href = '/index.html'
				}

			}).catch(function(error) {
				console.error(error)
			})

			// if(true){
			// 	return true;
			// }
			// if(this.check_phone()&& this.check_username()){
			// 	var url=this.host+'/register/'
			// 	var data={
			// 		username:this.username,
			// 		mobile:this.mobile
			// 	}
			// 	axios.post(url,data,{
			// 		responType:'json',

			// 	}).then(function(resp){
			// 		if(resp.data.code==200){
			// 			window.location.href='index.htlm'
			// 		}
			// 	})
			// }
		}
	}
})
