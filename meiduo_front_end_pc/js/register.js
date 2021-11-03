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
		error_image_code_message:'',
		error_image_code:'',
		image_code:'',
		sms_code:'',
		error_sms_code:'',
		error_sms_code_message:'',
		allow:'',
		error_allow:'',
		check_image_code:'',
		image_code_url:'',

	},
	mounted: function() {
		this.generate_image_code()
	},
	// 用户名
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
			this.image_code_url = this.host + "/image_codes/"+ this.uuid+'/';
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
		// 手机号
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
		// 密码重复
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
		// 注册
		on_submit: (function(){
			if (this.error_name == false && this.error_password == false && this.error_check_password == false && this.error_phone == false){
				axios.post(this.host + '/register/',{
					username:this.username,
					password:this.password,
					password2:this.password2,
					mobile:this.mobile,
					allow:this.allow},
					{
						responseType:'json',
						withCredentials:true,
					})
					.then(responseType => {
						if (responseType.data.code ==200){
							alert(responseType.data.errmsg)
						}
						if (responseType.data.code == 400){
							alert(responseType.data.errmsg)
						}
					})


				}
		})
	}
})