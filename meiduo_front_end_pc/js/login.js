var app = new Vue({
    el: '#app',
    data:{
        host:host,
        username:'',
        error_username:'',
        password:'',
        error_pwd:'',
        error_pwd_message:'',
        remember:'',
        qq_login:'',
        error_username_message:''


    },
    methods:{
        check_username:function(){
            var reg = /^[A-Za-z0-9]{4,40}$/;
            if (reg.test(this.username)){
                this.error_username = false;
                return true;
            }else {
                this.error_username = true;
                this.error_username_message='用户名或手机号不规范'
            }
        },
        check_pwd:function(){
            var reg =/^[a-zA-Z0-9]\w{5,17}$/;
            if (!reg.test(this.password)){
                this.error_pwd = true;
                this.error_pwd_message='密码不符合规则'
                return false
            }else{
                this.error_pwd = false;
                return true;
            }
        },
        on_submit:function(){
            var url = this.host + '/login/'
            var data={
                username:this.username,
                password:this.password,
                remember:this.remember
            }
            var conf ={
                responseType:'json',
                withCredentials:true,
            }
            axios.post(url,data,conf).then(function(resp){
                if(resp.data.code==0){
                    window.location.href='/index.html'
                }else if(resp.data.cede == 400){
                    alert(resp.data.errmsg)
                }
                else{
                    alert('系统异常')
                }
            }).catch(function(err){
                // console.log(ree)
            })
        }

    }
})