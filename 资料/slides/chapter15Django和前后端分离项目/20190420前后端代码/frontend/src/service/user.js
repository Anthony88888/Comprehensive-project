import axios from 'axios';
import store from 'store';
import expire from 'store/plugins/expire';
import { observable } from 'mobx';

store.addPlugin(expire);

const AUTH_EXPIRE = 8 * 3600 * 1000;

class UserService {
  @observable loggedin = false; // 被观察对象
  @observable errMsg = '';

  login(email, password) {
    console.log(email, password);
    // => django ajax /api/user/login

    axios.post('/api/user/login', {
      email: email,
      password: password
    })
      .then(response => {
        console.log(response.data, '~~~~~~~~~~~~~~~~~~~~~~');
        const { user, token } = response.data;
        console.log(user, token);

        store.set('token', token, new Date().getTime + AUTH_EXPIRE);
        this.loggedin = true; // 被观察对象被修改
      })
      .catch(error => {
        //console.log(error);
        this.errMsg = '登录失败';

      });
  }

  reg(name, email, password) {
    console.log(name, email, password);
    // => django ajax /api/user/reg

    axios.post('/api/user/reg', {
      name:name,
      email: email,
      password: password
    })
      .then(response => {
        console.log(response.data, '~~~~~~~~~~~~~~~~~~~~~~');
        const token = response.data.token;
        console.log(token);

        store.set('token', token, new Date().getTime + AUTH_EXPIRE);
        this.loggedin = true; // 被观察对象被修改
      })
      .catch(error => {
        //console.log(error);
        this.errMsg = '注册失败';
      });
  }

}

const userService = new UserService();
export {userService};



