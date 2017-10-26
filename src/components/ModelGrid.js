import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'
import {
} from 'reactstrap';

class ModelGrid extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.url;
        document.title = this.props.name + " - BGDB";
        this.state = {
            models: []
        };
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
        return <h1>{this.type}</h1>;
    }

}

export default ModelGrid;
