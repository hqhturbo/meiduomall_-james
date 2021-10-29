var app = new Vue({
  el: '#app',
  data: {
    username: '',
    error_name: false,
    error_name_message:''
  },
  methods: {
    check_username: function () {
      // let that = this
      axios.get('http://127.0.0.1:8000/usernames?username=' + this.username).then(function (rsg){
        //alert(data.data.count)
        console.log(rsg.data.count)
        if (rsg.data.count == 1) {
          app.error_name_message = '用户名重复了';
          console.log(this.error_name_message)
          app.error_name = true;
        }
        else {
          app.error_name = false;
        }
      })
    }
  }
})
