var app = new Vue({
	el: "#app",
	data: {
		username:'',

		error_username:'',
		password:'',

		error_pwd:'',
		error_pwd_message:'',
		remember:'',
		qq_login:'',
	},
	methods:{
		check_username: function() {
		    var reg = /^[A-Za-z0-9]{4,40}$/;
		    if (reg.test(this.username)){
		    	this.error_username = false;
		    	return true;
			}else {
			    this.error_username = true;
			    return false;
			}
		},
		check_pwd: function() {
		    var reg = /^[a-zA-Z]\w{5,17}$/;
		    if (!reg.test(this.password)) {
		    	this.error_pwd = true;
		    	this.error_pwd_message = '密码不符合规定'
				return false;
            }else {
                this.error_pwd = false;
                return true
            }
		}

	},
})