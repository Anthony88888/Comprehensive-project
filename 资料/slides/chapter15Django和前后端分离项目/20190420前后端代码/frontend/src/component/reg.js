import React from 'react';
import '../css/login.css';
import { Link, Redirect } from 'react-router-dom';
import {userService as service} from '../service/user';
import { observer } from 'mobx-react';
import { message } from 'antd';

import 'antd/lib/message/style';
import { inject } from '../utils';

@inject({service})
@observer
export default class Reg extends React.Component {
    validate(password, confirmpwd) {
        return password.value === confirmpwd.value;
    }

    handleClick(event) {
        event.preventDefault();
        const form = event.target.form;
        const [name = '', email = '', password = '', confirmpwd = ''] = event.target.form;
        // if (!this.validate(password, confirmpwd))
        //     return 

        this.props.service.reg(name.value, email.value, password.value);
        console.log('in login handleclick +++++');
    }

    render() {
        console.log('Reg render <<<<<<<<<<<<<');
        if (this.props.service.loggedin) {
            return <Redirect to='/' />
        }

        let em = this.props.service.errMsg;

        return (
            <div className="login-page">
                <div className="form">
                    <form className="register-form">
                        <input type="text" placeholder="姓名" />
                        <input type="text" placeholder="邮箱" />
                        <input type="password" placeholder="密码" />
                        <input type="password" placeholder="确认密码" />
                        <button onClick={this.handleClick.bind(this)}>注册</button>
                        <p className="message">如果已经注册<Link to='/login'>请登录</Link></p>
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