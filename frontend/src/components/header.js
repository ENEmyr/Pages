import React, { Component } from 'react';
import { Link } from "react-router-dom";
import logo from '../logo.png';

class Header extends Component {
  render() {
    return (
      <div>
        <nav class="navbar navbar-light bg-light">
          <a class="navbar-brand" href="#">
            <img src={logo} width="30" height="30" class="d-inline-block align-top" alt="" />
            Instrapage {"   "}
            <Link to="/search">Search</Link> |{" "}
            <Link to="/setting">Setting</Link>
          </a>
          <form class="form-inline">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Login</button> &nbsp;
            <button class="btn btn-outline-secondary my-2 my-sm-0" type="submit" onClick={this.onRegisterClick}>Register</button>
          </form>
        </nav>
      </div>
    );
  }
  onRegisterClick() {
    window.open("/register");
  }
}

export default Header;
