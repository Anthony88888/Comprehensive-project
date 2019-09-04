import React from 'react';
import ReactDom from 'react-dom';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Menu, Icon, Layout, LocaleProvider } from 'antd';
import Pub from './component/pub';
import L from './component/list';
const { Header, Content, Footer } = Layout;

import zhCN from 'antd/lib/locale-provider/zh_CN';
import Login from './component/login';
import Reg from './component/reg';

import 'antd/lib/menu/style';
import 'antd/lib/icon/style';
import 'antd/lib/layout/style';
import Detail from './component/detail';


function Home() {
  return <h2>主页</h2>;
}

function About() {
  return <h2>关于我公司</h2>;
}

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <Menu
            theme="light"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            style={{ lineHeight: '64px' }}
          >
            <Menu.Item key="home">
              <Link to="/"><Icon type="home" />主页</Link>
            </Menu.Item>
            <Menu.Item key="login">
              <Link to="/login"><Icon type="login" />登录</Link>
            </Menu.Item>
            <Menu.Item key="reg">
              <Link to="/reg">注册</Link>
            </Menu.Item>
            <Menu.Item key="pub">
              <Link to="/pub/">发布</Link>
            </Menu.Item>
            <Menu.Item key="list">
              <Link to="/list/"><Icon type="bars" />文章列表</Link>
            </Menu.Item>
            <Menu.Item key="about">
              <Link to="/about">关于</Link>
            </Menu.Item>
          </Menu>
        </Header>

        <Content style={{ padding: '8px 50px' }}>
          <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
            <Route path="/" exact component={Home} />
            <Route path="/login/" component={Login} />
            <Route path="/reg/" component={Reg} />
            <Route path="/pub/" component={Pub} />
            <Route path="/list/" component={L} />
            <Route path="/post/:id" component={Detail} />
            <Route path="/about/" component={About} />
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          马哥教育 ©2008-2019
    </Footer>
      </Layout>
    </Router>
  );
}


ReactDom.render(<LocaleProvider locale={zhCN}>
  <App />
</LocaleProvider>, document.getElementById('root'));


