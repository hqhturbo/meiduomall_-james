var app = new Vue({
    el:'#app',
    data:{
        host,
        is_show_waiting:'',
        access_token:'',
        mobile:'',
        error_phone:false,
        error_phone_message:'',
        password:'',
        error_password:false,
        image_code:'',
        image_code_url:'',
        error_image_code:false,
        error_image_code_message:'',
        sms_code:'',
        sms_code_tip:'获取短信验证码',
        error_sms_code:'',
        error_sms_code_message:'',
        sending_flag:false,
    },
    mounted:function () {
        this.generate_image_code();
        // 从路径中获取qq重定向返回的code
        var code = this.get_query_string('code');
        axios.get(this.host + '/oauth_callback/?code=' + code, {
            responseType: 'json',
            withCredentials:true,
        })
            .then(asg => {
                if (asg.data.code==0){
                    location.href = '/index.html'
                }else{
                    this.access_token=asg.data.access_token
                    console.log(this.access_token)
                }

            })
    },

    methods:{
        // 获取url路径参数
        get_query_string: function(name){
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        generate_image_code: function () {
            this.image_code_id = generateUUID();
            this.image_code_url = this.host + '/image_codes/' + this.image_code_id + '/'
        },

        check_phone:function (){
            if (!/^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$/.test(this.mobile)) {
                this.error_phone_message = '手机号码格式错误';
                this.error_phone = true;
            } else {
                this.error_phone = false;
            }
        },
        check_pwd:function () {
            if (!/^\w{8,20}$/.test(this.password)) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_image_code:function () {
            if (!this.image_code) {
                this.error_image_code_message = '请输入图片验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },
        check_sms_code:function () {
            if (!this.sms_code) {
                this.error_sms_code_message = '请输入短信验证码';
                this.error_sms_code = true
            } else {
                this.error_sms_code = false
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
        on_submit:function () {
            this.check_phone();
            this.check_pwd();
            this.check_image_code();
            this.check_sms_code();

            if (this.error_phone == false && this.error_password == false && this.error_image_code ==false
            && this.error_sms_code == false) {
                axios.post(this.host + '/oauth_callback/',{
                    mobile:this.mobile,
                    password:this.password,
                    sms_code:this.sms_code,
                    access_token:this.access_token
                },{
                    responseType:'json',
                    withCredentials: true
                })
                    .then(asg => {
                        if (asg.data.code == 0){
                            location.href = '/index.html'
                        }
                        if (asg.data.code == 400){
                            alert(asg.data.errmsg)
                        }
                    })

            }
        },
    }
})