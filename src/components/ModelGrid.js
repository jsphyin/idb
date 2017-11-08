import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link,
    Redirect
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
    CardSubtitle,
    Button,
    ButtonGroup
} from 'reactstrap';

class ModelGrid extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.url;
        document.title = this.props.name + " - BGDB";
        this.state = {
            models: [],
            page: 1,
            total_pages: 3
        };
        this.host = 'http://boardgamedb.me';
        if(window.location.hostname === 'localhost') {
            this.host = '';
        }
        var query = props.location.search
        var model = props.name.toLowerCase()
        this.api_url = this.host + '/api/' + model + query;
        this.url = this.host + '/' + model + query;
        fetch(this.api_url, {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                this.setState({
                    page: json.page,
                    total_pages: json.total_pages,
                    models: json.results
                });
            });
    }

    parse_query(query) {
        var params = [];
        params = query.split('&')
        for(var i = 0; i < params.length; i++) {
            params[i] = params[i].split('=');
        }
        return params;
    }

    gen_query(params) {
        var query = '';
        for(var i = 0; i < params.length; i++) {
            if(i > 0) {
                query += '&';
            }
            query += params[i][0] + '=' + params[i][1];
        }
        return query;
    }

    fetch_page(page_number) {
        if(this.state.page != page_number && page_number >= 1 && page_number <= this.state.total_pages) {
            var api_url = this.api_url.split('?')
            var url = this.url.split('?')
            if(url.length > 1) {
                var params = this.parse_query(url[1])
                var found = false;
                for(var i = 0; i < params.length; i++) {
                    if(params[i][0] === 'page') {
                        params[i][1] = page_number;
                        found = true;
                        break;
                    }
                }
                if(!found) {
                    api_url = this.api_url + '&page=' + page_number;
                    this.props.history.push(this.url + '&page=' + page_number);
                } else {
                    api_url = api_url[0] + '?' + this.gen_query(params);
                    this.props.history.push(url[0] + '?' + this.gen_query(params));
                }
            } else {
                api_url = api_url[0] + '?page=' + page_number;
                this.props.history.push(url[0] + '?page=' + page_number);
            }
            fetch(api_url, {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    this.setState({
                        page: json.page,
                        total_pages: json.total_pages,
                        models: json.results
                    });
                });
        }
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
            fontWeight: 'bold'
        };

        const grid_model_attribute = {
            textAlign: 'left'
        };
        var rows = []
        for(var i = 0; i < this.state.models.length; i++) {
            var model = this.state.models[i];
            switch(this.props.name) {
                case "Games":
                    var devs = <div>Unknown Developer</div>;
                    if (model.developers.length > 0) {
                        devs = <div>Developed by <Link to={'/developer/' + model.developers[0][0]}>{model.developers[0][1]}</Link></div>;
                    }
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>{devs}</li>
                            <li>{model.min_players} - {model.max_players} Players</li>
                            <li>Released in {model.year}</li>
                            <li>Rated {model.rating}/10</li>
                        </ul>
                    );
                    break;
                case "Genres":
                    var devs = <div>No notable devs</div>;
                    if (model.developers.length > 0) {
                        devs = <div>Notable Dev: <Link to={'/developer/' + model.developers[0][0]}>{model.developers[0][1]}</Link></div>;
                    }
                    var games = <div>No notable games</div>;
                    if (model.games.length > 0) {
                        games = <div>Notable Games: <Link to={'/game/' + model.games[0][0]}>{model.games[0][1]}</Link></div>;
                    }
                    var events = <div>No events</div>;
                    if (model.events.length > 0) {
                        events = <div>Events: <Link to={'/event/' + model.events[0][0]}>{model.events[0][1]}</Link></div>;
                    }
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>{devs}</li>
                            <li>{games}</li>
                            <li>{events}</li>
                        </ul>
                    );
                    break;
                case "Developers":
                    var genres = <div>No Genres</div>;
                    if (model.genres.length > 0) {
                        genres = <div>Genres: <Link to={'/genre/' + model.genres[0][0]}>{model.genres[0][1]}</Link></div>;
                    }
                    var games = <div>No notable games</div>;
                    if (model.games.length > 0) {
                        games = <div>Notable Games: <Link to={'/game/' + model.games[0][0]}>{model.games[0][1]}</Link></div>;
                    }
                    var website = <a href={model.website}>{model.website}</a>;
                    if (model.website === null) {
                        website = <div>No website</div>;
                    }
                    rows.push(
                        <ul style={grid_model_attribute}>
                            <li>{genres}</li>
                            <li>{games}</li>
                            <li>{website}</li>
                        </ul>
                    );
                    break;
                case "Events":
                    var val = <div>No Games or Genres</div>
                    if (model.games.length > 0) {
                        val = <Link to={'/game/' + model.games[0][0]}>{model.games[0][1]}</Link>;
                    } else if(model.genres.length > 0) {
                        val = <Link to={'/genre/' + model.genres[0][0]}>{model.genres[0][1]}</Link>;
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
        var pages = [];
        var show_pages = 2;
        for(var i = -show_pages; i <= show_pages; i++) {
            if(this.state.page + i >= 1 && this.state.page + i <= this.state.total_pages) {
                pages.push(this.state.page + i)
            }
        }
        var pagination = (
            <ButtonGroup>
            <Button color="secondary" onClick={() => this.fetch_page(1)}>{"<<"}</Button>
            <Button color="secondary" onClick={() => this.fetch_page(this.state.page - 1)}>{"<"}</Button>
            {pages.map(function(page, i) {
                return (
                    <Button key={i} color={this.state.page == page ? "primary" : "secondary"} onClick={() => this.fetch_page(page)}>{page}</Button>
                );
            }, this)}
            <Button color="secondary" onClick={() => this.fetch_page(this.state.page + 1)}>{">"}</Button>
            <Button color="secondary" onClick={() => this.fetch_page(this.state.total_pages)}>{">>"}</Button>
            </ButtonGroup>
        );
        return (
            <div className="container">
                <div style={page_header}>
                    <h2>{this.props.name}</h2>
                    <Row>
                        {pagination}
                    </Row>
                </div>
                <section>
                    <Row>
                    {this.state.models.map(function(model, i) {
                        return (
                                <Card key={i} style={grid_model}>
                                    <Link to={'/' + this.props.name.toLowerCase().slice(0, this.props.name.length - 1) + '/' + model.id}>
                                    <CardImg style={grid_model_img} src={model.img}/>
                                    </Link>
                                    <CardBody>
                                        <strong><span style={grid_model_name}>{model.name}</span></strong>
                                        {rows[i]}
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
