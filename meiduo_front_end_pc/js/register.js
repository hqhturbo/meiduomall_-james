var app = new Vue({
  el: '#app',
  data: {
    host: host,
    username: '',
    error_name: false,
    error_name_message: '',
    error_password: false,
    password: '',
    password2: '',
    error_check_password: false,
    error_phone: false,
    mobile: '',
    error_phone_message: '',
    uuid: '',
    image_code: '',
    error_image_code: false,
    error_image_code_message: '',
    image_code_url: '',
    allow: false,
    sms_code: '',
    error_sms_code: '',
    sms_code_tip: '点击获取验证码',
    sending_flag: false, // 正在发送短信标志
    error_allow: false,
    error_sms_code_message: '',
    sms_status: '',
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
      if (this.error_name == false) {
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
    check_pwd: function () {
      if (!/^\w{8,20}$/.test(this.password)) {
        this.error_password = true
      } else {
        this.error_password = false
      }
    },
    // 确认密码
    check_cpwd: function () {
      if (this.password != this.password2) {
        this.error_check_password = true
      } else {
        this.error_check_password = false
      }
    },
    // 手机号
    check_phone: function () {
      if (!/^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/.test(this.mobile)) {
        this.error_phone_message = '请输入正确的手机号码'
        this.error_phone = true
      } else {
        this.error_phone = false
      }
      if (this.error_phone == false) {
        axios.get(this.host + '/mobiles/' + this.mobile + '/count/').then(function (resp) {
          if (resp.data.count == 1) {
            app.error_phone_message = '该手机号已存在'
            console.log(this.error_phone_message)
            app.error_phone = true
          } else {
            app.error_phone = false
          }
        })
      }
    },
    generate_image_code: function () {
      this.uuid = generateUUID()
      this.image_code_url = this.host + '/imgs/' + this.uuid + '/'
    },
    check_image_code: function () {
      if (!this.image_code) {
        this.error_image_code_message = '请输入图片验证码'
        this.error_image_code = true
      } else {
        this.error_image_code = false
      }
    },
    on_submit: function () {
      this.check_username();
      this.check_pwd();
      this.check_cpwd();
      this.check_phone();
      if (this.error_name == false && this.error_password == false && this.error_check_password == false
          && this.error_phone == false && this.error_sms_code == false) {
        axios.post(this.host + '/register/', {
          'username': this.username,
          'password': this.password,
          'password2': this.password2,
          'mobile': this.mobile,
          'sms_code':this.sms_code
        }, {
          responseType: 'json',
          withCredentials: true,
        })
            .then(rsg => {
              if (rsg.data.code == 200) {
                location.href = 'index.html'
              }
              if (rsg.data.code == 400) {
                alert(rsg.data.errmsg)
              }
            })
      }
    },
    send_sms_code: function () {
      if (this.sening_flag == true) {
        return;
      }
      this.sending_flag = true
      this.check_phone()
      if (this.error_phone == true) {
        this.sending_flag = false;
        return;
      }
      axios.get(this.host + '/sms_codes/' + this.mobile + '/' + '?image_code=' + this.image_code + '&uuid=' + this.uuid, {
        responseType: 'json',
        withCredentials: true
      })
          .then(rsg=>{
            if (rsg.data.code==400){
              this.error_sms_code = true;
              this.error_sms_code_message = rsg.data.errmsg;
              return;
            }
            // 表示后端发送短信成功
            // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
            var num = 60;
            // 设置一个计时器
            this.sms_status = 'pointer-events:none; opacity: 0.7'
            var t = setInterval(() => {
              if (num == 1) {
                // 如果计时器到最后, 清除计时器对象
                app.sms_status = ''
                clearInterval(t);
                // 将点击获取验证码的按钮展示的文本回复成原始文本
                this.sms_code_tip = '获取短信验证码';
                // 将点击按钮的onclick事件函数恢复回去
                this.sending_flag = false;
              } else {
                num -= 1;
                // 展示倒计时信息
                this.sms_code_tip = num + '秒';
              }
            }, 1000, 60)
          })
    },
    check_sms_code: function () {
      if (!this.sms_code) {
        this.error_sms_code_message = '请填写短信验证码';
        this.error_sms_code = true;
      } else {
        this.error_sms_code = false;
      }
    },
    check_allow: function () {
      if (!this.allow) {
        this.error_allow = true;
      } else {
        this.error_allow = false;
      }
    },
  }
})
