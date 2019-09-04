import React from 'react';
import BraftEditor from 'braft-editor';
import { Form, Input, Icon, Button, message } from 'antd';
import { inject } from '../utils';
import { observer } from 'mobx-react';
import { postService as service } from '../service/post';


import 'antd/lib/message/style';
import 'antd/lib/form/style';
import 'antd/lib/icon/style';
import 'antd/lib/button/style';
import 'antd/lib/input/style';
import 'braft-editor/dist/index.css';

const { TextArea } = Input;

@inject({ service }) // PostService
@observer
export default class Pub extends React.Component {
    state = {
        editorState: BraftEditor.createEditorState('<p>Hello <b>World!</b></p>'), // 设置编辑器初始内容
        outputHTML: '<p></p>'
    }

    handleSubmit(e) {
        e.preventDefault();
        const [title] = e.target; //form 解构 []
        if (title.value)
            this.props.service.pub(title.value, this.state.outputHTML);
    }

    handleChange = (editorState) => {
        this.setState({
            editorState: editorState,
            outputHTML: editorState.toHTML()
        })
    }

    render() {
        let msg = this.props.service.msg;
        const formItemLayout = {
            labelCol: { span: 4 },
            wrapperCol: { span: 14 }
        };
        const { editorState, outputHTML } = this.state;
        return (<Form {...formItemLayout} onSubmit={this.handleSubmit.bind(this)}>
            <Form.Item label="标题">
                <Input />
            </Form.Item>
            <Form.Item wrapperCol={{ span: 18 }} label="正文">
                <BraftEditor
                    value={editorState}
                    onChange={this.handleChange.bind(this)}
                />
            </Form.Item>
            <Form.Item wrapperCol={{ span: 18, offset: 4 }}>
                <Button type="primary" htmlType="submit">发布</Button>
            </Form.Item>
            <div className="output-content">{outputHTML}</div>
        </Form>);
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.service.msg)
            message.info(prevProps.service.msg, 3, () => prevProps.service.msg = '');
    }
}



