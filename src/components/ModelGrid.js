import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'
import {
    Row,
    Col,
    Card,
    CardTitle,
    CardText,
    CardHeader,
    CardBody,
    CardFooter,
    CardImg,
    CardSubtitle
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
                this.setState({
                    models: json
                });
            });
    }

    render() {
        const page_header = {
            paddingTop: '20px'
        };

        const grid_model = {
            textAlign: 'center',
            margin: '20px',
            width: '300px',
            height: '400px'
        };

        const grid_model_img = {
            width: '300px',
            height: '200px'
        };

        const grid_model_name = {
            fontWeight: 'old'
        };

        const grid_model_attribute = {
            textAlign: 'left'
        };
        var rows = []
        for(var i = 0; i < this.state.models.length; i++) {
            var model = this.state.models[i];
            console.log(model.developers);
            switch(this.props.name) {
                case "Games":
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>Developed by <Link to={'/developer/' + model.developers[0][0]}>{model.developers[0][1]}</Link></li>
                            <li>{model.min_players} - {model.max_players} Players</li>
                            <li>Released in {model.year}</li>
                            <li>Rated {model.rating}/10</li>
                        </ul>
                    );
                    break;
                case "Genres":
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>Notable Dev: <Link to={'/developer/' + model.developers[0][0]}>{model.developers[0][1]}</Link></li>
                        </ul>
                    );
                    break;
                case "Developers":
                    rows.push(
                        <ul style={grid_model_attribute}>
                        </ul>
                    );
                    break;
                case "Events":
                    var val = <div></div>
                    if (model.games.length > 0) {
                        val = model.games[0][1];
                    } else {
                        val = model.genres[0][1];
                    }
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>Time: {model.time}</li>
                            <li>At {model.location}</li>
                            <li>{val}</li>
                            <li><a href={model.link}>Meetup Link</a></li>
                        </ul>
                    );
                    break;
            }
        }
        return (
            <div class="container">
                <div style={page_header}>
                    <h2>{this.props.name}</h2>
                    <section id="grid-description">
                        {this.props.desc}
                    </section>
                </div>
                <section>
                    <Row>
                    {this.state.models.map(function(model, i) {
                        return (
                                <Card style={grid_model}>
                                    <Link to={'/' + this.props.name.toLowerCase() + '/' + model.id}>
                                    <CardImg style={grid_model_img} src={model.img}/>
                                    </Link>
                                    <CardBody>
                                        <CardText>
                                            <strong><span style={grid_model_name}>{model.name}</span></strong>
                                            {rows[i]}
                                        </CardText>
                                    </CardBody>
                                </Card>
                        );
                    }, this)}
                    </Row>
                </section>
            </div>
        );
    }

}
export default ModelGrid;
