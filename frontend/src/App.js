import React, { Component } from 'react';
import { Link } from "react-router-dom";


class App extends Component {
  render() {
    return (
      <div>
        <h1 style={{ textAlign: "center" }}>Instrapage</h1>
        <nav
            style={{
                borderBottom: "solid 1px",
                paddingBottom: "1rem"
            }}
        >
            <Link to="/search">Search</Link> |{" "}
            <Link to="/setting">Setting</Link>
        </nav>
      </div>
    );
  }
}

export default App;
