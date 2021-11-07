var app = new Vue({
  el:'#app',
  data:{
    username:'',
    host:host,
    error_username:false,
    password:'',
    error_pwd:'',
    error_pwd_message:'',
    remember:'',
    qq_login:''
  },
  methods:{
    check_username:function (){
      if (!/^[A-Za-z0-9]{5,11}$/.test(this.username)) {
        this.error_username = true;
        return false;
      } else {
        this.error_username = false;
        return true;
      }
    },
    check_pwd:function (){
      if (!/^\w{8,20}$/.test(this.password)) {
        this.error_pwd_message = '密码不符合规则'
        this.error_pwd = true
        return false;
      } else {
        this.error_pwd = false
        return true
      }
    },
    on_submit:function (){
      var url=this.host + '/login/'
      var data = {
        'username':this.username,
        'password':this.password,
        'remember':this.remember
      }
      var conf = {
        responseType: 'json',
        withCredentials: true,
      }
      axios.post(url,data,conf).then(rsg=>{
        if(rsg.data.code == 0){
          location.href = 'index.html'
        }
        else if(rsg.data.code=400){
          alert(rsg.data.errmsg)
        }
        else{
          alert('系统异常')
        }
      }).catch(rep=>{
        alert(rep.data.errmsg)
      })
    }
  }
})