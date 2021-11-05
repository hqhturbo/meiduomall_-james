var app = new Vue({
    el:'#app',
    data:{
        host,
        username:''
    },
    mounted:function(){
        //获取cookie中的用户名
        // alert($cookies.get('username'))
        let u_json=$cookies.get('username') //使用第三方库进行cookie获取
        let u_str=JSON.parse(u_json) //将数据进行json反序列化
        this.username = eval(u_str) //将uncode编码转为中文
    },
    methods:{
        logoutfunc:function () {
            var url = this.host + '/logout/'
            console.log(url)
            axios.delete(url, {
                responseType: 'json',
                withCredentials: true,
            })
                .then(asg => {
                    if (asg.data.code==200){
                        location.href='/login.html'
                    }else{
                        alert('系统异常')
                    }
            })
                .catch(error => {

                })
        }
    }
})