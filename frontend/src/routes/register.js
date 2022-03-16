import React, { Component } from 'react';
import axios from 'axios'

import Header from "../components/header";


class Register extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.email = React.createRef();
        this.password = React.createRef();
        this.confirmPass = React.createRef();
        this.firstName = React.createRef();
        this.lastName = React.createRef();
        this.penName = React.createRef();
    }
    componentDidMount() {

    }
    render() {
        return (
            <div>
                <Header />
                <div className='container'>
                    <h1>Register</h1>
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
                        <div class="form-group row">
                            <label for="inputPassword" class="col-sm-2 col-form-label">Confirm Password</label>
                            <div class="col-sm-10">
                                <input type="password" class="form-control" id="confirmPassword" placeholder="Confirm Password" ref={this.confirmPass} />
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="inputPassword" class="col-sm-2 col-form-label">First Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="firstName" placeholder="First Name" ref={this.firstName} />
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="inputPassword" class="col-sm-2 col-form-label">Last Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="firstName" placeholder="Last Name" ref={this.lastName} />
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="inputPassword" class="col-sm-2 col-form-label">Pen Name</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="penName" placeholder="Pen Name" ref={this.penName} />
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
        console.log(this.confirmPass)
        if (this.confirmPass.current.value != this.password.current.value) {
            alert('password confirm not correct');
            return;
        }
        const apiUrl = 'https://api.pages.dogmatism.me/users/register';
        const { email, password, firstName, lastName, penName } = this;
        axios.post(apiUrl, {
            email: email.current.value,
            password: password.current.value,
            first_name: firstName.current.value,
            last_name: lastName.current.value,
            penname: penName.current.value,
            image_url: "/images/default.png",
        }).then((response) => {
            alert('register success')
        }).catch((error) => {
            alert('error ' + error)
        });
    }
}

export default Register;
