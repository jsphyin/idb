import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'
import {
    Navbar,
    NavItem,
    NavbarBrand,
    Nav,
    NavLink,
    InputGroup,
    Input,
    InputGroupAddon,
    Col
} from 'reactstrap';

class Model extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.params.url;
        this.id   = props.match.params.id;
        this.state = {
            data: []
        };
        console.log('123');
        this.host = 'http://boardgamedb.me';
        if(window.location.hostname === 'localhost') {
            this.host = '';
        }
        fetch(this.host + '/api' + props.match.url, {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                console.log(json)
                this.state.models = json;
            });
    }

    render() {
        return <h1>{this.type} {this.id}</h1>;
    }

}

export default Model;
