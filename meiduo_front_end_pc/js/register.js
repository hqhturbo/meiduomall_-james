var app = new Vue({
  el: '#app',
  data: {
    host:host,
    username: '',
    error_name: false,
    error_name_message: '',
    error_password: false,
    password:'',
    password2:'',
    error_check_password:false,
    error_phone:false,
    mobile:'',
    error_phone_message:'',
    uuid:'',
    image_code:'',
    error_image_code:false,
    error_image_code_message:'',
    image_code_url:'',
  },
  mounted() {
    this.generate_image_code()
  },
  methods: {
    // 用户名
    check_username: function () {
      if (!/^[A-Za-z0-9]{5,11}$/.test(this.username)) {
        this.error_name_message = '用户必须5到10位的数字或字母';
        this.error_name = true;
      } else {
        this.error_name = false;
      }
      if(this.error_name==false){
        axios.get(this.host + '/usernames/' + this.username + '/count/').then(function (rsg) {
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
    },
    // 手机号
    check_phone:function (){
      if (!/^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/.test(this.mobile)){
        this.error_phone_message = '请输入正确的手机号码'
        this.error_phone = true
      }
      else {
        this.error_phone = false
      }
      if(this.error_phone==false){
        axios.get(this.host + '/mobiles/' + this.mobile + '/count/').then(function (resp){
          if (resp.data.count==1){
            app.error_phone_message = '该手机号已存在'
            console.log(this.error_phone_message)
            app.error_phone = true
          }
          else{
            app.error_phone = false
          }
        })
      }
    },
    generate_image_code:function (){
      this.uuid = generateUUID()
      this.image_code_url = this.host + '/imgs/' + this.uuid + '/'
    },
    check_image_code:function () {
      if (!this.image_code){
        this.error_image_code_message = '请输入图片验证码'
        this.error_image_code = true
      }
      else {
        this.error_image_code = false
      }
    },
    on_submit:function(){
      this.check_username();
      this.check_pwd();
      this.check_cpwd();
      this.check_phone();
      if (this.error_name == false && this.error_password == false && this.error_check_password == false
          && this.error_phone == false){
        axios.post(this.host + '/register/',{
          'username': this.username,
          'password': this.password,
          'password2': this.password2,
          'mobile': this.mobile
        },{
          responseType: 'json',
          withCredentials:true,
        }).then(rsg=>{
          alert(rsg.data.errmsg)
        })
      }
    },
  }
})
