var app = new Vue({
  el: '#app',
  data: {
    username: '',
    error_name: false,
    error_name_message: '',
    error_password: false,
    password:'',
    password2:'',
    error_check_password:false
  },
  methods: {
    // 用户名
    check_username: function () {
      if (!/^[A-Za-z0-9]{5,10}$/.test(this.username)) {
        this.error_name_message = '用户必须5到10位的数字或字母';
        this.error_name = true;
      } else {
        this.error_name = false;
      }
      if(this.error_name==false){
        axios.get('http://127.0.0.1:8000/usernames?username=' + this.username).then(function (rsg) {
          //alert(data.data.count)
          if (rsg.data.count == 1) {
            app.error_name_message = '用户名重复了';
            app.error_name = true;
          } else {
            app.error_name = false;
          }
        })
      }
    },
    // 密码
    check_pwd:function (){
      if (!/^\w{8,20}$/.test(this.password)){
        this.error_password = true
      }
      else {
        this.error_password = false
      }
    },
    // 确认密码
    check_cpwd:function (){
      if (this.password!=this.password2){
        this.error_check_password = true
      }
      else {
        this.error_check_password = false
      }
    }
  }
})
