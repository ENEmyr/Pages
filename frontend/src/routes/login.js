import React, { Component } from 'react';
import axios from 'axios'

import Header from "../components/header";


class Login extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.email = React.createRef();
        this.password = React.createRef();
    }
    componentDidMount() {

    }
    render() {
        return (
            <div>
                <Header />
                <div className='container'>
                    <h1>Login</h1>
                    <form onSubmit={this.handleSubmit}>
                        <div class="form-group row">
                            <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="email" placeholder="email@example.com" ref={this.email} />
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
                            <div class="col-sm-10">
                                <input type="password" class="form-control" id="password" placeholder="Password" ref={this.password} />
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
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

export default Login;
