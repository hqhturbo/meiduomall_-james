var app=new Vue({
	el:'#app',
	data:{
		username:'',
		qq_login:'',
		remember:'',
		// check_username:'',
		error_username:'',
		password:'',
		error_pwd:'',
		// check_pwd:'',
		error_pwd_message:'',
		host:host
	},
	methods:{
		check_username:function(){
			var reg = /^[A-Za-z0-9]{5,11}/;
			if(reg.test(this.username)){
				this.error_username = false;
				return true;
			}else{
				this.error_username = true;
				return false;
			}
		},
		check_pwd:function(){
			var reg = /^[a-zA-Z]\w{5,17}$/;
			if (!reg.test(this.password)){
				this.error_pwd = true;
				this.error_pwd_message='密码不符合规则'
				return false;
			}else{
				this.error_pwd = false;
				return true
			}
		},
		on_submit:function(){
			var url=this.host+'/login/'
			var data={
				username:this.username,
				password:this.password,
				remembered:this.remember
			}
			var conf={
				responseType:'json',
				withCredentials:true,
			}
			axios.post(url,data,conf).then(function(resp){
				if(resp.data.code==0){
					window.location.href='/index.html'
				}else if(resp.data.code==400){
					alert(resp.data.errmsg)
				}
				else{
					alert('系统异常')
				}
			}).catch(function(err){
				console.log(err)
			})
		}
	}
})