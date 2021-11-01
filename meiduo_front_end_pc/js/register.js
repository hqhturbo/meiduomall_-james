var app = new Vue({
	el: "#app",
	data: {
		// 用户名
		username: '',
		host:host,
		error_name: '',
		error_name_message: '',
		// 手机验证
		mobile:'',
		error_phone:'',
		error_phone_message:'',
		// 密码
		error_password:'',
		password:'',
		error_password_message:'',
		// 确认密码
		error_password2_message:'',
		password2:'',
		error_check_password:'',
// 同意协议
		allow:'',
		error_allow:'',

	},
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
		check_phone: function(msg) {
			if (!/^[0-9]{11}/.test(this.mobile)){
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
		check_pwd: function (){
			if (!/^\w{8,20}/.test(this.password)){
				this.error_password_message = '请输入8-20为的英文字母、数字、下划线的密码'
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
		}

	}
})