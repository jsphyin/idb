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

class NavBar extends React.Component {

    render() {
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
                        <InputGroup>
                        <Input placeholder="Search" />
                        <InputGroupAddon> <span className="fa fa-search"></span> </InputGroupAddon>
                        </InputGroup>
                    </Col>
            </Navbar>
        );
    }
}

export default NavBar;
