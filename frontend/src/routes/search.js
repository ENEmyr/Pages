import React, { Component } from 'react';
import { Link } from "react-router-dom";

import Header from "../components/header";


class App extends Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.state = {
            listData: [{
                "id": 1,
                "text": "Devpulse"
            }, {
                "id": 2,
                "text": "Linklinks"
            }, {
                "id": 3,
                "text": "Centizu"
            }, {
                "id": 4,
                "text": "Dynabox"
            }, {
                "id": 5,
                "text": "Avaveo"
            }, {
                "id": 6,
                "text": "Demivee"
            }, {
                "id": 7,
                "text": "Jayo"
            }, {
                "id": 8,
                "text": "Blognation"
            }, {
                "id": 9,
                "text": "Podcat"
            }, {
                "id": 10,
                "text": "Layo"
            }],
            filteredListData: []
        }
        
    }
    componentDidMount(){
        this.setState({ filteredListData: this.state.listData });
    }
    render() {
        return (
            <div>
                <Header />
                <h1>React Search</h1>
                <div className="search">
                    <form>
                        <label>
                            Search:
                            <input type="text" name="name" onChange={this.handleChange} />
                        </label>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
                <ul>
                    {this.state.filteredListData.map((item) => (
                        <li key={item.id}>{item.text}</li>
                    ))}
                </ul>
            </div>
        );
    }
    handleChange(event) {
        this.setState({ filteredListData: this.state.listData })
        let filteredListData = this.state.listData.filter(element => element.text.includes(event.target.value))
        this.setState({ filteredListData });
    }
}

export default App;
