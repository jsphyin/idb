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
        this.type = props.match.params.type;
        this.id   = props.match.params.id;
    }

    render() {
        return <h1>{this.type} {this.id}</h1>;
    }

}

export default Model;
