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
    CardSubtitle,
    Button,
    ButtonGroup,
} from 'reactstrap';

class Search extends React.Component {

    constructor(props) {
        super(props)
        this.params = this.parse_query(props.location.search)
        this.params['per_page'] = 9;
        this.state = {
            query: '',
            page: 0,
            total_pages: Infinity,
            models: [],
            loading: false
        }
        this.fetch_page('page' in this.params ? this.params['page'] : 1, true)
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

    fetch_page(page_number, force_fetch = false) {
        if(force_fetch || (this.state.page != page_number && page_number >= 1
            && page_number <= this.state.total_pages)) {
            // Set page number in params
            this.params['page'] = page_number;
            if('query' in this.params) {
                this.state.query = this.params['query']
            } else if('search-input' in this.params) {
                this.state.query = this.params['search-input']
                delete this.params['search-input']
                this.params['query'] = this.state.query
            } else if('search-button' in this.params) {
                this.state.query = this.params['search-button']
                delete this.params['search-button']
                this.params['query'] = this.state.query
            } else {
                this.state.query = ''
                this.setState(this.state)
                return;
            }

            // Generate query
            let query = this.gen_query(this.params);

            // Set URL
            this.props.history.push('/search' + query);
            this.state.loading = true;

            // Fetch new grid model data
            fetch('/api/search' + query, {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    this.state.page = json.page;
                    this.state.total_pages = json.total_pages;
                    this.models = []
                    var count = 0;
                    for(let i = 0; i < json.results.length; i++) {
                        fetch('/api/' + json.results[i].type + 's/' + json.results[i].id, {method: 'GET'})
                            .then(r => r.json())
                            .then(j => {
                                j.type = json.results[i].type
                                this.state.models.push(j)
                                count += 1
                                if(count == json.results.length) {
                                    this.state.loading = false
                                    this.setState(this.state)
                                }
                            });
                    }
                });
        }
    }

    render() {
        var no_results = ''
        if(this.state.models.length == 0 && !this.state.loading) {
            no_results = (
                <h1 style={{textAlign: 'center', margin: '20px'}}>
                    No Results
                </h1>
            );
        }
        var rows = []
        for(var i = 0; i < this.state.models.length; i++) {
            var model = this.state.models[i];
            switch(model.type) {
                case "game":
                    var devs = <div>Unknown Developer</div>;
                    if (model.developers.length > 0) {
                        devs = <div>Developed by <Link to={'/developer/' + model.developers[0][0]}>{model.developers[0][1]}</Link></div>;
                    }
                    rows.push(
                        <ul className='model-attribute'>
                            <li>{devs}</li>
                            <li>{model.min_players} - {model.max_players} Players</li>
                            <li>Released in {model.year}</li>
                            <li>Rated {model.rating}/10</li>
                        </ul>
                    );
                    break;
                case "genre":
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
                        <ul className='model-attribute'>
                            <li>{devs}</li>
                            <li>{games}</li>
                            <li>{events}</li>
                        </ul>
                    );
                    break;
                case "developer":
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
                        <ul className='model-attribute'>
                            <li>{genres}</li>
                            <li>{games}</li>
                            <li>{website}</li>
                        </ul>
                    );
                    break;
                case "event":
                    var val = <div>No Games or Genres</div>
                    if (model.games.length > 0) {
                        val = <Link to={'/game/' + model.games[0][0]}>{model.games[0][1]}</Link>;
                    } else if(model.genres.length > 0) {
                        val = <Link to={'/genre/' + model.genres[0][0]}>{model.genres[0][1]}</Link>;
                    }
                    rows.push(
                        <ul className='model-attribute'>
                            <li>Time: {model.time}</li>
                            <li>At {model.location}</li>
                            <li>{val}</li>
                            <li><a href={model.link}>Meetup Link</a></li>
                        </ul>
                    );
                    break;
            }
        }

        // Pagination
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
            <Button color={this.state.page == this.state.total_pages || this.state.total_pages == 0 ? "secondary" : ""} onClick={() => this.fetch_page(this.state.page + 1)}>{">"}</Button>
            <Button color={this.state.page == this.state.total_pages || this.state.total_pages == 0 ? "secondary" : ""} onClick={() => this.fetch_page(this.state.total_pages)}>{">>"}</Button>
            </ButtonGroup>
        );
        return (
            <div className="container">
                <div className='page-header'>
                    <Card>
                        <CardHeader>
                            <Row className="justify-content-md-center">
                                <h1>{this.state.query === '' ? "No Search Query" : "Search Results for: '" + this.state.query + "'"}</h1>
                            </Row>
                        </CardHeader>
                    </Card>
                </div>
                <section>
                    <Row className="justify-content-md-center">
                    {this.state.models.map(function(model, i) {
                        return (
                                <Card key={i} className='grid-model'>
                                    <Link to={'/' + model.type + '/' + model.id}>
                                    <CardImg className='grid-model-img' src={model.img !== null ? model.img : 'https://cf.geekdo-images.com/images/pic1657689_t.jpg'}/>
                                    </Link>
                                    <CardBody>
                                        <strong><span className='model-name'>{model.name}</span></strong>
                                        {rows[i]}
                                    </CardBody>
                                </Card>
                        );
                    }, this)}
                    </Row>
                {no_results}
                </section>
                <Row className="justify-content-md-center page-footer">
                    <Col className="col-md-auto">
                        {pagination}
                    </Col>
                </Row>
            </div>
        )
    }

}

export default Search;
