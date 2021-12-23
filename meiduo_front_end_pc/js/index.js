var app=new Vue({
	el:'#app',
	data:{
		username:'',
		host:host
	},
	mounted:function(){
		var u_json=$cookies.get('username')
		var u_str=JSON.parse(u_json)
		this.username=eval(u_str)
	},
	methods:{
		logoutfunc:function(){
			var url=this.host+'/logout/'
			var conf = {
				responseType:'json',
				withCredentials:true,
			}
			axios.delete(url,conf).then(function(resp){
				if(resp.data.code==200){
					window.location.href='/login.html'
				}else{
					alert('系统异常')
				}
			}).catch(function(err){
				console(err)
			})
		}
	}
})