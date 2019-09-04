
import React from 'react';
import { inject } from '../utils';
import { observer } from 'mobx-react';
import { postService as service } from '../service/post';
import { Link } from "react-router-dom";
import { Card } from 'antd';


import 'antd/lib/card/style';



@inject({ service }) // PostService
@observer
export default class Detail extends React.Component {
    constructor(props) {
        super(props);
        
        const {id=-1} = props.match.params;
        // 去数据库中找详情
        console.log(id);
        props.service.getPost(id);
    }
    render() {
        const {post_id, title, postdate, author, author_id, content} = this.props.service.post;
        if (title){
            return (<Card
                title={title}
                extra={<a href={"/user/" + author_id}>{author}</a>}
                style={{ width: '80%' }}
              >
                <p>{postdate}</p>
                <p dangerouslySetInnerHTML={{__html:content}}></p>
              </Card>);
        } else {
            return (<div>无数据</div>);
        }
    }
}






