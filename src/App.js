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
                    <Route path='/about' component={About}/>

                    <Route path='/game' component={(props) => (<Model {...props} name="Games"/>)}/>
                    <Route path='/genre' component={(props) => (<Model {...props} name="Genres"/>)}/>
                    <Route path='/developer' component={(props) => (<Model {...props} name="Developers"/>)}/>
                    <Route path='/event' component={(props) => (<Model {...props} name="Events"/>)}/>

                    <Route path='/games' component={(props) => (<ModelGrid {...props} name="Games"/>)}/>
                    <Route path='/genres' component={(props) => (<ModelGrid {...props} name="Genres"/>)}/>
                    <Route path='/developers' component={(props) => (<ModelGrid {...props} name="Developers"/>)}/>
                    <Route path='/events' component={(props) => (<ModelGrid {...props} name="Events"/>)}/>

                </div>
            </Router>
        );
    }
}

export default App;
