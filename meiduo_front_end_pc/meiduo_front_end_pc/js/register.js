var app=new Vue({
	el:'#app',
	data:{
		username:'',
		error_name:'',
		error_name_message:''
	},
	methods:{
		check_username:function(resp){
			var that=this;
			var username=that.username
			// var reg=/^[0-9]$/
			
			// console.log(new RegExp().test(reg,username))
			// if (reg.test(username)==false)
			// {
			// 	that.error_name_message='用户名不合法'
			// 	that.error_name=true
			// 	return
			// }
			axios.get('http://127.0.0.1:8000/usernames/'+username+'/count/',{responseType:'json'})
			.then(function(resp){
				that.error_name_message=resp.data.errmsg
				console.log(resp)
				if(resp.data.code==200){
					that.error_name=true
				}else{
					that.error_name=false
				}
			}).catch(function(err){
				console.log(err)
			})
		}
	}
})