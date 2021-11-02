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
		// error_image_code_message:'',
		// error_image_code:'',
		// image_code:'',
		// sms_code:'',
		// error_sms_code:'',
		// error_sms_code_message:'',
		allow:'',
		error_allow:''
	},
	// 用户名
	methods: {
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