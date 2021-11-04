var app = new Vue({
    el:'#app',
    data: {
        host,
        username:'',
        error_username:false,
        password:'',
        error_pwd:false,
        error_pwd_message:'',
        remember:false,
    },
    methods:{
        //账号
        check_username:function () {
            if (!/^[A-Za-z0-9]{5,10}$/.test(this.username)) {
                this.error_username=true;
            }else{
                this.error_username=false;
            }
        },
        //密码
        check_pwd:function () {
            if (!/^\w{8,20}$/.test(this.password)) {
                this.error_pwd_message='请输入密码'
                this.error_pwd = true
            }else{
                this.error_pwd = false
            }
        },

        //判断是否记住密码
        check_remember:function () {
            if (!this.remember){
                this.remember = false;
            }else{
                this.remember = true;
            }
        },
        //登录
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            this.check_remember();

            //点击注册发送请求
            if (this.error_username == false || this.error_pwd == false) {
                axios.post(this.host + '/login/',{
                    username:this.username,
                    password:this.password,
                    remember:this.remember,
                }, {
                    responseType:'json'
                })
                    .then(asg => {
                        if (asg.data.code == 0) {
                            location.href = '/index.html'
                        } else {
                            this.error_pwd_message = asg.data.errmsg;
                            this.error_pwd = true;
                        }
                    })
            }
        },

        //qq登录
        qq_login:function () {

        },
    }
})