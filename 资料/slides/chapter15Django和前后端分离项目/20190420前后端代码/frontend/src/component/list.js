import React from 'react';
import { inject, parse_qs } from '../utils';
import { observer } from 'mobx-react';
import { postService as service } from '../service/post';
import { Link } from "react-router-dom";
import { List } from 'antd';


import 'antd/lib/list/style';
@inject({ service }) // PostService
@observer
export default class L extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
        const search = props.location.search;
        props.service.list(search);
    }

    handleChange(page, pageSize) {
        this.props.service.list(`?size=${pageSize}&page=${page}`);
    }

    getParams(page) {
        console.log(this.props, '++++++++++++++++++++++++++');
        const search = this.props.location.search;
        const { size = 20 } = parse_qs(search); //?page=5
        return `/list/?page=${page}&size=${size}`
    }

    handleItemRender(page, type, originalElement) {
        if (page === 0)
            return originalElement;
        if (type === 'prev')
            return <Link className="ant-pagination-item-link" to={this.getParams(page)}>&lt;</Link>;
        if (type === 'next')
            return <Link className="ant-pagination-item-link" to={this.getParams(page)}>&gt;</Link>;
        if (type === 'page')
            return <Link to={this.getParams(page)}>{page}</Link>;

    }

    render() {
        const { posts: data = [], pagination = {} } = this.props.service.posts;

        const { page: current = 1, size: pageSize = 20, count: total = 0 } = pagination;

        return (<List
            size="large"
            header="文章列表"
            bordered
            dataSource={data}
            renderItem={item => (<List.Item><Link to={"/post/" + item.post_id}>{item.title}</Link></List.Item>)}
            pagination={{
                onChange: this.handleChange.bind(this),
                pageSize: pageSize,
                total: total,
                current: current,
                itemRender: this.handleItemRender.bind(this)
            }}
        />);

        //return (<div>无数据</div>);

    }
}
