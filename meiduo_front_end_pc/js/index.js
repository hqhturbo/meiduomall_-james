var app = new Vue({
  el:'#app',
  data:{
    username:'',
    host:'host'
  },
  mounted:function (){
    var u_json = $cookies.get('username') //使用第三方库进行获取cookie
    var u_str = JSON.parse(u_json) // 将数据进行json反序列化
    this.username = eval(u_str) //将uncode编码转为中文
  },
  methods:{
    logoutfunc:function (){
      var url = this.host + '/logout/'
      var conf = {
        responseType: 'json',
        withCredentials: true,
      }
      axios.delete(url,conf).then(rsg=>{
        if (rsg.data.code == 200){
          location.href = 'login.html'
        }else{
          alert('系统异常')
        }
      }).catch(rsp=>{
        console.log(rsp)
      })
    }
  }
})