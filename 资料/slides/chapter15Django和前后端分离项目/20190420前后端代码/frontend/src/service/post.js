import axios from 'axios';
import store from 'store';

import { observable } from 'mobx';

class PostService {
    constructor() {
        this.axios = axios.create({
            baseURL: '/api/post/'
        });
    }

    @observable msg = ''; // 被观察对象
    @observable posts = {};
    @observable post = {};

    getJwt() {
        console.log(store.get('token', null));
        return store.get('token', null);
    }


    pub(title, content) {
        // => django ajax /api/post/pub

        axios.post('/api/post/pub', {
            title, content
        }, {
                headers: { 'Jwt': this.getJwt() }
            })
            .then(response => {
                console.log(response.data, '~~~~~~~~~~~~~~~~~~~~~~');
                //const { user, token } = response.data;
                this.msg = '发布成功'; // 被观察对象被修改
            })
            .catch(error => {
                //console.log(error);
                this.msg = '发布失败';

            });
    }

    list(search) {
        // => django ajax /api/post/

        this.axios.get(search)
            .then(response => {
                this.posts = response.data;
                //this.msg = '发布成功'; // 被观察对象被修改
            })
            .catch(error => {
                //console.log(error);
                this.msg = '发布失败';

            });
    }

    getPost(id) {
        // => django ajax /api/post/123

        this.axios.get(id)
            .then(response => {
                //this.posts = response.data;
                this.post = response.data.post;
                this.msg = '发布成功'; // 被观察对象被修改
            })
            .catch(error => {
                //console.log(error);
                this.msg = '发布失败';

            });
    }

}


const postService = new PostService();
export { postService };

















