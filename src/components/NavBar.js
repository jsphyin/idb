import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link,
    Redirect
} from 'react-router-dom'
import {
    Navbar,
    NavItem,
    NavbarBrand,
    Nav,
    NavLink,
    Form,
    FormGroup,
    Input,
    InputGroup,
    InputGroupButton,
    Button,
    Col
} from 'reactstrap';

class NavBar extends React.Component {

    constructor(props) {
        super(props)
        var query = window.location.href.split('?')
        if(query.length > 1) {
            this.params = this.parse_query('?' + query[1])
        } else {
            this.params = {}
        }
    }

    // Returns object with keys -> values
    parse_query(query) {
        if(query === '') {
            return [];
        }
        var params = {};
        var query_params = query.slice(1, query.length).split('&')
        for(var i = 0; i < query_params.length; i++) {
            var param = query_params[i].split('=');
            if(param.length > 1) {
                params[param[0]] = param[1];
            }
        }
        return params;
    }

    render() {
        var query = window.location.href.split('?')
        if(query.length > 1) {
            this.params = this.parse_query('?' + query[1])
        } else {
            this.params = {}
        }
        if(window.location.href.indexOf('search') === -1 && 'query' in this.params && this.params['query'] !== '') {
            console.log(this.params)
            return <Redirect push to={'/search?query=' + this.params['query']} />
        }
        return (
            <Navbar color="faded" light expand="lg" className="container-fluid bg-light">
                <NavbarBrand id='nav-logo' href="/">BGDB</NavbarBrand>
                    <Col className="mr-auto">
                    <Nav className="mr-auto">
                        <NavItem>
                            <NavLink id="nav-home" tag={Link} className="text-dark" to="/">Home</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink id="nav-games" tag={Link} className="text-dark" to="/games">Games</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink id="nav-genres" tag={Link} className="text-dark" to="/genres">Genres</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink id="nav-developers" tag={Link} className="text-dark" to="/developers">Developers</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink id="nav-events" tag={Link} className="text-dark" to="/events">Events</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink id="nav-about" tag={Link} className="text-dark" to="/about">About</NavLink>
                        </NavItem>
                    </Nav>
                    </Col>
                    <Col className="col-md-3 mr-auto">
                        <Form>
                            <FormGroup>
                                <InputGroup>
                                    <Input id='search-input' name='query' placeholder="Search" />
                                    <InputGroupButton><Button id='search-button' className="fa fa-search"></Button></InputGroupButton>
                                </InputGroup>
                            </FormGroup>
                        </Form>
                    </Col>
            </Navbar>
        );
    }
}

export default NavBar;
