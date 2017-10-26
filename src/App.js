import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'

import NavBar    from './components/NavBar';
import ModelGrid from './components/ModelGrid';
import Model     from './components/Model';
import Home      from './components/Home';
import About     from './components/About';

class App extends React.Component {
    render() {
        return (
            <Router>
                <div id="wrapper" class="container-fluid">
                    <NavBar />
                    <Route exact path='/' component={Home}/>
                    <Route path='/games' component={(props) => (<ModelGrid {...props} name="Games"/>)}/>
                    <Route path='/genres' component={(props) => (<ModelGrid {...props} name="Genres"/>)}/>
                    <Route path='/developers' component={(props) => (<ModelGrid {...props} name="Developers"/>)}/>
                    <Route path='/events' component={(props) => (<ModelGrid {...props} name="Events"/>)}/>
                    <Route path='/about' component={About}/>
                    <Route path='/games/:id' component={Model}/>
                    <Route path='/genres/:id' component={Model}/>
                    <Route path='/developers/:id' component={Model}/>
                    <Route path='/events/:id' component={Model}/>
                </div>
            </Router>
        );
    }
}

/*
    <Route path='/about' component={About}/>
*/
export default App;
