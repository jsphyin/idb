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
import MultiSelect from './MultiSelect'

class ModelGrid extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.url;
        document.title = this.props.name + " - BGDB";
        this.state = {
            models: [],
            page: 0,
            total_pages: Infinity,
            filter_options: []
        };
        this.host = 'http://boardgamedb.me';
        if(window.location.hostname === 'localhost') {
            this.host = '';
        }
        this.params = this.parse_query(props.location.search)
        this.params['per_page'] = 18;
        this.model = props.name.toLowerCase()
        this.fetch_page('page' in this.params ? this.params['page'] : 1);
        fetch(this.host + '/api/' + this.model + '/names', {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                var filter_options = []
                for(var i = 0; i < json.length; i++) {
                    filter_options.push({
                        label: json[i][1],
                        value: json[i][0]
                    });
                }
                this.state.filter_options = filter_options;
                this.setState(this.state);
            });
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

    // Generates query string
    gen_query(params) {
        var query = '?';
        var keys = Object.keys(params);
        for(var i = 0; i < keys.length; i++) {
            if(i > 0) {
                query += '&';
            }
            query += keys[i] + '=' + params[keys[i]];
        }
        return query;
    }

    fetch_page(page_number) {
        if(this.state.page != page_number && page_number >= 1
            && page_number <= this.state.total_pages) {

            // Set page number in params
            this.params['page'] = page_number;

            // Generate query
            var query = this.gen_query(this.params);

            // Set URL
            this.props.history.push(this.host + '/' + this.model + query);

            // Fetch new grid model data
            fetch(this.host + '/api/' + this.model + query, {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    this.state.page = json.page;
                    this.state.total_pages = json.total_pages;
                    this.state.models = json.results;
                    this.setState(this.state);
                });
        }
    }

    render() {
        const page_header = {
            paddingTop: '20px'
        };

        const page_footer = {
            paddingBottom: '20px'
        };

        const grid_model = {
            textAlign: 'center',
            margin: '20px',
            width: '300px',
            height: '440px'
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
            <Button color={this.state.page == 1 ? "secondary" : ""} onClick={() => this.fetch_page(1)}>{"<<"}</Button>
            <Button color={this.state.page == 1 ? "secondary" : ""} onClick={() => this.fetch_page(this.state.page - 1)}>{"<"}</Button>
            {pages.map(function(page, i) {
                return (
                    <Button key={i} color={this.state.page == page ? "link" : ""} onClick={() => this.fetch_page(page)}>{page}</Button>
                );
            }, this)}
            <Button color={this.state.page == this.state.total_pages ? "secondary" : ""} onClick={() => this.fetch_page(this.state.page + 1)}>{">"}</Button>
            <Button color={this.state.page == this.state.total_pages ? "secondary" : ""} onClick={() => this.fetch_page(this.state.total_pages)}>{">>"}</Button>
            </ButtonGroup>
        );
        return (
            <div className="container">
                <div style={page_header}>
                    <Card>
                        <CardHeader>
                            <Row className="justify-content-md-center">
                                <h1>{this.props.name}</h1>
                            </Row>
                        </CardHeader>
                        <Row className="justify-content-md-center">
                            <Col>
                                <MultiSelect options={this.state.filter_options} name="Banana" />
                            </Col>
                        </Row>
                    </Card>
                </div>
                <section>
                    <Row className="justify-content-md-center">
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
                <Row className="justify-content-md-center" style={page_footer}>
                    <Col className="col-md-auto">
                        {pagination}
                    </Col>
                </Row>
            </div>
        );
    }

}
export default ModelGrid;
