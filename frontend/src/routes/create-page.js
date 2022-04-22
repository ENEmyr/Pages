import React, { Component } from 'react';
import axios from 'axios'

import Header from "../components/header";

import { EditorState } from 'draft-js';
import { Editor } from 'react-draft-wysiwyg';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';


class CreatePage extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = { editorState: EditorState.createEmpty() };
    }
    componentDidMount() {

    }
    onEditorStateChange = (editorState) => {
        this.setState({
            editorState,
        });
    }
    render() {
        return (
            <div>
                <Header />
                <div className='container'>
                    <header className="App-header">
                        Page Editor
                    </header>
                    <Editor
                        editorState={this.state.editorState}
                        onEditorStateChange={this.onEditorStateChange}
                        wrapperClassName="wrapper-class"
                        editorClassName="editor-class"
                        toolbarClassName="toolbar-class"
                    />
                </div>
            </div>
        );
    }
    handleSubmit(event) {
        event.preventDefault();
        const apiUrl = 'https://api.pages.dogmatism.me/users/signin';
        const { email, password } = this;
        axios.post(apiUrl, {
            email: email.current.value,
            password: password.current.value,
        }).then((response) => {
            alert('login success');
        }).catch((error) => {
            console.log(error.response);
            if (error.response) alert('error ' + error.response.data.detail[0].msg);
            else alert('error ' + error);
        });
    }
}

export default CreatePage;
