import React from 'react';
import '../css/login.css';
import {Link, Redirect} from 'react-router-dom';
import {userService as service} from '../service/user';
import {observer} from 'mobx-react';
import { message } from 'antd';

import 'antd/lib/message/style';
import { inject } from '../utils';



@inject({service})
@observer
export default class Login extends React.Component {

    handleClick(event) {
        event.preventDefault();
        const form = event.target.form;
        console.log(this);
        this.props.service.login(form[0].value, form[1].value);
        //this.props.service.handle(this); // async 
        //this.props.service.loggedin
        console.log('in login handleclick +++++');
    }

    render() {// 要求必须使用一下被观察对象，用什么被观察对象，就相当于注册了关注谁
        console.log('Login render <<<<<<<<<<<<<');
        if (this.props.service.loggedin) {
            return <Redirect to='/' />
        }

        let em = this.props.service.errMsg;

        return (
            <div className="login-page">
                <div className="form">
                <form className="login-form">
                    <input type="text" placeholder="邮箱" defaultValue='wayne@magedu.com' />
                    <input type="password" placeholder="密码" defaultValue="abc1" />
                    <button onClick={this.handleClick.bind(this)}>登录</button>
                    <p className="message">还未注册？ <Link to='/reg'>请注册</Link></p>
                </form>
                </div>
            </div>
        );
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.service.errMsg)
            message.info(prevProps.service.errMsg, 3, ()=>prevProps.service.errMsg='');
    }

}









