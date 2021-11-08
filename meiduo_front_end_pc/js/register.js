var app = new Vue({
	el: "#app",
	data: {
		username: '',
		host:host,
		error_name: '',
		error_name_message: '',
		mobile:'',
		error_phone:'',
		error_phone_message:'',
		password:'',
		error_password:'',
		error_password_message :'',
		password2:'',
		error_check_password:'',
		error_password2_message:'',
		image_code:'',
		image_code_url:'',
		error_image_code:'',
		error_image_code_message:'',
		allow:false,
		error_allow:'',
		sms_code:'',
		error_sms_code_message:'',
		sms_code_tip:'点击获取短信验证码',
		error_sms_code:'',


	},

	mounted(){
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
					// console.error(response.data.code)
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
							error_image_code_message = response.data.errmsg
							alert(error_image_code_message)
							// this.image_code_error = true;
						}
						alert(Response.data.errmsg)
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
		check_username: function(resp) {
			if(!/^[A-Za-z0-9]{5,11}/.test(this.username)){
				this.error_name_message = '用户名格式出错了'
				this.error_name = true
			}
			else {
				this.error_name = false
			}
			if(this.error_name==false){
				axios.get(this.host + '/usernames/' + this.username + '/count/').then(resp=> {
					if (resp.data.count == 1) {
						this.error_name_message = '用户名重复了'
						this.error_name=true
					}else{
						this.error_name=false
					}
				})
			}
		},
		check_phone: function(msg) {
			if (!/^1[345789]\d{9}$/.test(this.mobile)){
				this.error_phone_message = '手机格式错误'
				this.error_phone = true
			}
			else {
				this.error_phone = false
			}
			if(this.error_phone==false){
				axios.get(this.host + '/mobiles/' + this.mobile + '/count/').then(msg=> {

					if (msg.data.count == 1) {
						this.error_phone_message = '手机号重复了'
						this.error_phone=true
					}else{
						this.error_phone=false
					}
				})
			}
		},
		check_pwd: function () {
			if (!/^\w{8,20}/.test(this.password)){
				this.error_password_message = '请输入8-20位的英文字母、数字、下划线的密码'
				this.error_password = true
			}
			else {
				this.error_password = false
			}
		},
		check_cpwd: function() {
		    if (this.password2 != this.password){
		    	this.error_password2_message = '两次密码不一致'
				this.error_check_password = true
			}else {
		    	this.error_check_password = false
			}
		},
		check_image_code:function () {
			if (!this.image_code){
			  this.error_image_code_message = '请输入图片验证码'
			  this.error_image_code = true
			}
			else {
			  this.error_image_code = false
			}
		  },
		  check_sms_code: function(){
			
		},

		on_submit: (function(){
			if (this.error_name == false && this.error_password == false && this.error_check_password == false && this.error_phone == false){
				axios.post(this.host + '/register/',{
					username:this.username,
					password:this.password,
					password2:this.password2,
					mobile:this.mobile,
					sms_code:this.sms_code,
					allow:this.allow},
					{
						responseType:'json',
						withCredentials:true,
					})
					.then(response => {
						if (response.data.code ==200){
							location.href = 'index.html';
						}
						if (response.data.code == 400){
							alert(response.data.errmsg)
						}
					})
					// .catch(error => {
					// 	if (error.response.code == 400){
					// 		if ('non_field_errors' in error){
					// 			this.error_sms_code_message = error.response;
					// 		}else{
					// 			this.error_sms_code_message = '数据有误';
					// 		}
					// 		this.error_sms_code = true;
					// 	}else {
					// 		console.log(error);
					// 	}
					// })
				}
		})
	}
})