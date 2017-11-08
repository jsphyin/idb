import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'
import {
    Card,
    CardImg,
    CardBody,
    CardText,
    Row,
    Col
} from 'reactstrap';

class Model extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.params.url;
        this.id   = props.match.params.id;
        this.state = {
            model: null
        };
        this.host = 'http://boardgamedb.me';
        if(window.location.hostname === 'localhost') {
            this.host = '';
        }
        var query = props.location.search
        var model = props.match.url.substring(1, props.match.url.length)
        if(model.charAt(model.length - 1) == '/') {
            model = model.substring(0, model.length - 1);
        }
        fetch(this.host + '/api/' + model + 's' + query, {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                this.setState({
                    model: json
                });
            });
    }

    render() {
        var model = this.state.model;
        if (model === null) { 
            return <div></div>;
        }
        const page_header = {
            paddingTop: '20px'
        };

        const grid_model = {
            textAlign: 'center',
            margin: '20px',
        };

        const grid_model_img = {
            width: '100%',
            height: '600px'
        };

        const grid_model_name = {
            fontWeight: 'bold'
        };

        const grid_model_attribute = {
            textAlign: 'left'
        };
        var attrib = <div></div>
        switch(this.props.name) {
            case "Games":
                var devs = <div>Unknown Developer</div>;
                if (model.developers.length > 0) {
                    devs = []
                    for(var i = 0; i < model.developers.length; i++) {
                        devs.push(<li>Developed by <Link to={'/developer?id=' + model.developers[i][0]}>{model.developers[i][1]}</Link></li>);
                    }
                }

                var pubs = <div>Unknown Publisher</div>;
                if (model.publishers.length > 0) {
                    pubs = []
                    for(var i = 0; i < model.publishers.length; i++) {
                        pubs.push(<li>Published by {model.publishers[i][1]}</li>);
                    }
                }

                var arts = <div>Unknown Artist</div>;
                if (model.artists.length > 0) {
                    arts = []
                    for(var i = 0; i < model.artists.length; i++) {
                        arts.push(<li>Art done by {model.artists[i][1]}</li>);
                    }
                }
                
                var names = <div>No alternate names</div>;
                if (model.alt_names.length > 0) {
                    names = []
                    for(var i = 0; i < model.alt_names.length; i++) {
                        names.push(<li>{model.alt_names[i]}</li>);
                    }
                }

                var fams = <div>No board game family</div>;
                if (model.families.length > 0) {
                    fams = []
                    for(var i = 0; i < model.families.length; i++) {
                        fams.push(<li>{model.families[i][1]}</li>);
                    }
                }

                var gens = <div>No genres</div>;
                if (model.genres.length > 0) {
                    gens = []
                    for(var i = 0; i < model.genres.length; i++) {
                        gens.push(<li>{model.genres[i][1]}</li>);
                    }
                }

                var mechs = <div>No mechanics</div>;
                if (model.mechanics.length > 0) {
                    mechs = []
                    for(var i = 0; i < model.mechanics.length; i++) {
                        mechs.push(<li>{model.mechanics[i][1]}</li>);
                    }
                }
                attrib = (
                    <div>
                        <h3>Alternate Names</h3>
                        <ul style={grid_model_attribute}>
                            {names}
                        </ul>
                        <h3>Description</h3>
                        <ul style={grid_model_attribute}>
                            {model.desc}
                        </ul>
                        <h3>Release Information</h3>
                        <ul style={grid_model_attribute}>
                            <li>Released in {model.year}</li>
                            {devs}
                            {pubs}
                            {arts}
                        </ul>
                        <h3>Genres and Mechanics</h3>
                        <ul style={grid_model_attribute}>
                            {gens}
                            {mechs}
                        </ul>
                        <h3>Play Information</h3>
                        <ul style={grid_model_attribute}>
                            <li>{model.min_players} - {model.max_players} Players</li>
                            <li>Rated {model.rating}/10</li>
                        </ul>
                        <h3>Board Game Families</h3>
                        <ul style={grid_model_attribute}>
                            {fams}
                        </ul>
                    </div>
                );
                break;
            case "Genres":
                var devs = <div>No Notable Developers</div>;
                if (model.developers.length > 0) {
                    devs = []
                    for(var i = 0; i < model.developers.length; i++) {
                        devs.push(<li><Link to={'/developer?id=' + model.developers[i][0]}>{model.developers[i][1]}</Link></li>);
                    }
                }

                var games = <div>No Notable Games</div>;
                if (model.games.length > 0) {
                    games = []
                    for(var i = 0; i < model.games.length; i++) {
                        games.push(<li><Link to={'/game?id=' + model.games[i][0]}>{model.games[i][1]}</Link></li>);
                    }
                }

                var events = <div>No Events</div>;
                if (model.events.length > 0) {
                    events = []
                    for(var i = 0; i < model.events.length; i++) {
                        events.push(<li><Link to={'/event?id=' + model.events[i][0]}>{model.events[i][1]}</Link></li>);
                    }
                }

                attrib = (
                    <div>
                        <h3>Description</h3>
                        <ul style={grid_model_attribute}>
                            {model.desc}
                        </ul>
                        <h3>Notable Developers</h3>
                        <ul style={grid_model_attribute}>
                            <li>{devs}</li>
                        </ul>
                        <h3>Notable Games</h3>
                        <ul style={grid_model_attribute}>
                            <li>{games}</li>
                        </ul>
                        <h3>Events</h3>
                        <ul style={grid_model_attribute}>
                            <li>{events}</li>
                        </ul>
                    </div>
                );
                break;
            case "Developers":
                var gens = <div>No genres</div>;
                if (model.genres.length > 0) {
                    gens = []
                    for(var i = 0; i < model.genres.length; i++) {
                        gens.push(<li>{model.genres[i][1]}</li>);
                    }
                }

                var games = <div>No Notable Games</div>;
                if (model.games.length > 0) {
                    games = []
                    for(var i = 0; i < model.games.length; i++) {
                        games.push(<li><Link to={'/game?id=' + model.games[i][0]}>{model.games[i][1]}</Link></li>);
                    }
                }


                var website = <a href={model.website}>{model.website}</a>;
                if (model.website === null) {
                    website = <li>No website</li>;
                }

                attrib = (
                    <div>
                        <h3>Description</h3>
                        <ul style={grid_model_attribute}>
                            {model.desc}
                        </ul>
                        <h3>Games</h3>
                        <ul style={grid_model_attribute}>
                            {games}
                        </ul>
                        <h3>Genres</h3>
                        <ul style={grid_model_attribute}>
                            {gens}
                        </ul>
                        <h3>Website Link</h3>
                        <ul style={grid_model_attribute}>
                            <li>{website}</li>
                        </ul>
                    </div>
                );
                break;
            case "Events":
                var val = <div>No Games or Genres</div>
                if (model.games.length > 0) {
                    val = <Link to={'/game?id=' + model.games[0][0]}>{model.games[0][1]}</Link>;
                } else if(model.genres.length > 0) {
                    val = <Link to={'/genre?id=' + model.genres[0][0]}>{model.genres[0][1]}</Link>;
                }
                attrib = (
                    <div>
                        <h3>Description</h3>
                        <ul style={grid_model_attribute}>
                            {model.desc}
                        </ul>
                        <h3>Meetup Information</h3>
                        <ul style={grid_model_attribute}>
                            <li>Time: {model.time}</li>
                            <li>At {model.location}</li>
                            <li><a href={model.link}>Meetup Link</a></li>
                        </ul>
                        <h3>Related Games or Genres</h3> 
                        <ul style={grid_model_attribute}>
                            <li>{val}</li>
                        </ul>
                    </div>
                );
                break;
        }
        return (
            <div class="container">
                <section>
                    <Card style={grid_model}>
                        <CardImg style={grid_model_img} src={model.img}/>
                        <CardBody>
                            <CardText>
                                <strong><h1 style={grid_model_name}>{model.name}</h1></strong>
                                {attrib}
                            </CardText>
                        </CardBody>
                    </Card>
                </section>
            </div>
        );
    }

}

export default Model;
