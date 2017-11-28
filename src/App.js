import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link,
	Redirect
} from 'react-router-dom'

import NavBar        from './components/NavBar';
import ModelGrid     from './components/ModelGrid';
import Model         from './components/Model';
import Home          from './components/Home';
import About         from './components/About';
import Search        from './components/Search';
import Visualization from './components/Visualization';

class App extends React.Component {
    render() {
        return (
            <Router>
                <div id="wrapper" className="container-fluid">
                    <NavBar />
                    <Route exact path='/' component={Home}/>
                    <Route path='/about' component={About}/>
                    <Route path='/search' component={(props) => (<Search {...props}/>)}/>

                    <Route path='/games' component={(props) => (<ModelGrid {...props} name="Games"/>)}/>
                    <Route path='/genres' component={(props) => (<ModelGrid {...props} name="Genres"/>)}/>
                    <Route path='/developers' component={(props) => (<ModelGrid {...props} name="Developers"/>)}/>
                    <Route path='/events' component={(props) => (<ModelGrid {...props} name="Events"/>)}/>
                    <Route path='/viz' component={Visualization}/>

                    <Route path='/game/:id' component={(props) => (<Model {...props} name="Games"/>)}/>
                    <Route path='/boardgame/:id/:name' render={( {match} ) => (<Redirect to={"/game/" + match.params.id}/>)}/>
                    <Route path='/boardgamedesigner/:id/:name' render={( {match} ) => (<Redirect to={"/developer/" + match.params.id}/>)}/>
					<Route path='/genre/:id' component={(props) => (<Model {...props} name="Genres"/>)}/>
                    <Route path='/developer/:id' component={(props) => (<Model {...props} name="Developers"/>)}/>
                    <Route path='/event/:id' component={(props) => (<Model {...props} name="Events"/>)}/>

                </div>
            </Router>
        );
    }
}

export default App;
