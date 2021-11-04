var app = new Vue({
    el: '#app',
    data: {
        host: host,
        username: '',
        error_name: false,
        error_name_message: '',
        password: '',
        error_password: false,
        password2: '',
        error_check_password: false,
        mobile: '',
        error_phone: false,
        error_phone_message: '',
        image_code: '',
        error_image_code: false,
        error_image_code_message: '',
        sms_code: '',
        sms_code_tip: '获取短信验证码',
        error_sms_code: false,
        error_sms_code_message: '',
        image_code_id: '',
        image_code_url: '',
        sending_flag: false,
        allow: false,
        error_allow: false,
    },
    mounted: function () {
        this.generate_image_code();
    },

    methods: {
        generate_image_code: function () {
            this.image_code_id = generateUUID();
            this.image_code_url = this.host + '/image_codes/' + this.image_code_id + '/'
        },
        //检查用户名
        check_username: function () {
            if (!/^[A-Za-z0-9]{5,10}$/.test(this.username)) {
                this.error_name_message = '用户名需是5到10位字母或数字'
                this.error_name = true
            } else {
                this.error_name = false
            }
            if (this.error_name === false) {
                axios.get(this.host + '/usernames/' + this.username + '/count/').then(asg => {
                    if (asg.data.count === 1) {
                        this.error_name_message = '用户名重复';
                        console.log(asg.data.count);
                        this.error_name = true;
                    } else {
                        this.error_name = false;
                    }
                })
            }
        },
        //检查密码是否合法
        check_pwd: function () {
            if (!/^\w{8,20}$/.test(this.password)) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        //检查两次密码是否相同
        check_cpwd: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },

        //检查手机号是否正确
        check_phone: function () {
            if (!/^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$/.test(this.mobile)) {
                this.error_phone_message = '手机号码格式错误';
                this.error_phone = true;
            } else {
                this.error_phone = false;
            }
            if (this.error_phone === false) {
                console.log(this.mobile)
                axios.get(this.host + '/mobile/' + this.mobile + '/count/').then(asg => {
                    if (asg.data.count === 1) {
                        this.error_phone_message = '手机号已存在';
                        this.error_phone = true;
                    } else {
                        this.error_phone = false;
                    }
                })
            }
        },

        // 判断是否输入图片验证码
        check_image_code: function () {
            if (!this.image_code) {
                this.error_image_code_message = '请输入图片验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },

        //判断是否输入短信验证码
        check_sms_code: function () {
            if (!this.sms_code) {
                this.error_sms_code_message = '请输入短信验证码';
                this.error_sms_code = true
            } else {
                this.error_sms_code = false
            }
        },

        //判断是否勾选用户协议
        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },

        //发送短信验证码
        send_sms_code: function () {
            if (this.sending_flag == true) {
                return;
            }
            this.sending_flag = true;
            //校验参数，保证输入款有值填写
            this.check_phone();
            this.check_image_code();

            if (this.error_phone == true || this.error_image_code == true) {
                this.sending_flag = false;
                return;
            }
            //向后端接口发送请求，让后端发送短信验证码
            axios.get(this.host + '/smscode/' + this.mobile + '/' + '?image_code=' + this.image_code +
                '&image_code_id=' + this.image_code_id, {
                responseType: 'json',
            })
                .then(response => {
                if (response.data.code === 200) {
                    //表示后端发送短信成功
                    //倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                    var num = 60;
                    //设置一个倒计时
                    var t = setInterval(() => {
                        if (num==1) {
                            //如果倒计时到最后，清除计时器对象
                            clearInterval(t)
                            //将点击获取验证码的按钮展示的文本回复成原始文本
                            this.sms_code_tip = '获取短信验证码'
                            //将点击按钮的onclick事件函数回复回去
                            this.sending_flag = false;
                        } else{
                            num -= 1;
                            //展示倒计时信息
                            this.sms_code_tip = num + '秒';
                        }
                    },1000,60)
                }else{
                    if (response.data.code === 400){
                        //图片验证码错误
                        this.error_image_code = true;
                        this.error_image_code_message = response.data.errmsg
                    }
                    this.error_sms_code = true;
                    this.generate_image_code();
                    this.sending_flag = false;
                }
            })
                .catch(error => {
                    if (error.data.status == 400){
                        this.error_sms_code_message = error.response.data.message;
                        this.error_sms_code = true;
                    }else{
                        console.log(error.response.data);
                    }
                    this.sending_flag = false;
                })
        },
        //注册
        on_submit: function () {
            this.check_username();
            this.check_phone();
            this.check_allow();
            this.check_pwd();
            this.check_cpwd();
            this.check_image_code();
            this.check_sms_code();

            //点击注册后发送请求
            if (this.error_name == false && this.error_phone == false && this.error_allow == false && this.error_password == false
                && this.error_check_password == false && this.error_image_code == false && this.error_sms_code == false) {
                axios.post(this.host + '/register/', {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    allow:this.allow
                }, {
                    responseType: 'json',
                    withCredentials: true,
                })
                    .then(asg => {
                        if (asg.data.code == 0) {
                            location.href = '/index.html'
                        }
                        if(asg.data.code == 400){
                            alert(asg.data.message)
                        }
                    })
                    .catch(error => {
                        if (error.response.code==400){
                            if ('non_field_errors' in error){
                                this.error_sms_code_message = error.response;
                            }else{
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code=true;
                        }else{
                            console.log(error);
                        }
                    })

            }
        }
    }
})
