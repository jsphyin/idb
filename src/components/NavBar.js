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
        if('search-input' in this.params && this.params['search-input'] !== '') {
            return <Redirect push to={'/search?query=' + this.params['search-input']} />
        }
        if('search-button' in this.params && this.params['search-button'] !== '') {
            return <Redirect push to={'/search?query=' + this.params['search-button']} />
        }
        return (
            <Navbar color="faded" light expand="lg" className="container-fluid bg-light">
                <NavbarBrand href="/">BGDB</NavbarBrand>
                    <Col className="mr-auto">
                    <Nav className="mr-auto">
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/">Home</Link></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/games">Games</Link></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/genres">Genres</Link></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/developers">Developers</Link></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/events">Events</Link></NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink><Link className="text-dark" to="/about">About</Link></NavLink>
                        </NavItem>
                    </Nav>
                    </Col>
                    <Col className="col-md-3 mr-auto">
                        <Form onSubmit={() => console.log("Yo")}>
                            <FormGroup>
                                <InputGroup>
                                    <Input name='search-button' placeholder="Search" />
                                    <InputGroupButton><Button className="fa fa-search"></Button></InputGroupButton>
                                </InputGroup>
                            </FormGroup>
                        </Form>
                    </Col>
            </Navbar>
        );
    }
}

export default NavBar;
