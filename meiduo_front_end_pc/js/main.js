import Axios from 'axios'
Vue.prototype.$axios = Axios
let getCookie = function (cookie) {
  let reg = /csrftoken=([\w]+)[;]?/g
  return reg.exec(cookie)[1]
}
Axios.interceptors.request.use(
    function(config) {
      // 在post请求前统一添加X-CSRFToken的header信息
      let cookie = document.cookie;
      if(cookie && config.method == 'post'){
        config.headers['X-CSRFToken'] = getCookie(cookie);
      }
      return config;
    },
    function(error) {
      // Do something with request error
      return Promise.reject(error);
    }
);
