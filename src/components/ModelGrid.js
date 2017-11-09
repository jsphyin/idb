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
    ButtonGroup,
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem
} from 'reactstrap';
import MultiSelect from './MultiSelect'

const filters = {
    'games': [
        {label: 'Developer', value: 'developers'},
        {label: 'Genre', value: 'genres'}
    ],
    'genres': [
        {label: 'Game', value: 'games'},
        {label: 'Developer', value: 'developers'}
    ],
    'developers': [
        {label: 'Game', value: 'games'},
        {label: 'Genre', value: 'genres'}
    ],
    'events': [
        {label: 'Game', value: 'games'},
        {label: 'Genre', value: 'genres'},
        {label: 'Location', value: 'events/locations'}
    ]
};

const sorts = {
    'games': [
        {label: 'Name ↑', value: '-name'},
        {label: 'Name ↓', value: 'name'}, 
        {label: 'Year ↑', value: '-year'},
        {label: 'Year ↓', value: 'year'}
    ],
    'genres': [
        {label: 'Name ↑', value: '-name'},
        {label: 'Name ↓', value: 'name'}, 
    ],
    'developers': [
        {label: 'Name ↑', value: '-name'},
        {label: 'Name ↓', value: 'name'}, 
    ],
    'events': [
        {label: 'Name ↑', value: '-name'},
        {label: 'Name ↓', value: 'name'}, 
        {label: 'Date ↑', value: '-time'},
        {label: 'Date ↓', value: 'time'}, 
    ]
};

class ModelGrid extends React.Component {
    
    constructor(props) {
        super(props);
        this.type = props.match.url;
        document.title = this.props.name + " - BGDB";
        this.state = {
            models: [],
            page: 0,
            total_pages: Infinity,
            filter_options: {},
            filterOpen: false,
            sortOpen: false,
            filter: {label: 'Filter by', value: ''},
            values: '',
            loading: false,
            sort: {label: 'Name ↓', value: 'name'}
        };
        this.params = this.parse_query(props.location.search)
        this.params['per_page'] = 18;
        this.model = props.name.toLowerCase()
        if(!('sort' in this.params)) {
            this.params['sort'] = this.state.sort.value
        } else {
            var found = false;
            for(var i = 0; i < sorts[this.model].length; i++) {
                if(this.params['sort'] === sorts[this.model][i].value) {
                    this.state.sort = sorts[this.model][i];
                    found = true;
                    break;
                }
            }
            if(!found) {
                this.params['sort'] = this.state.sort.value
            }
        }
        this.fetch_page('page' in this.params ? this.params['page'] : 1);
        for(let i = 0; i < filters[this.model].length; i++) {
            let filter = filters[this.model][i]
            fetch('/api/' + filter.value + '/names', {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    var filter_options = []
                    for(var j = 0; j < json.length; j++) {
                        filter_options.push({
                            label: json[j][1],
                            value: json[j][0].toString()
                        });
                    }
                    this.state.filter_options[filter.value] = filter_options;
                    let filter_param = filter.value.split('/')
                    filter_param = filter_param[filter_param.length - 1]
                    if(filter_param in this.params) {
                        this.state.values = decodeURI(this.params[filter_param])
                        this.state.filter = filter;
                    }
                    this.setState(this.state);
                });
        }
    }

    set_values(values) {
        this.state.values = values;
        if(values === '') {
            var filter = this.state.filter.value.split('/')
            filter = filter[filter.length-1]
            delete this.params[filter]
        } else {
            for(var i = 0; i < filters[this.model].length; i++) {
                var filter = filters[this.model][i].value.split('/')
                filter = filter[filter.length-1]
                if(filter in this.params && filter !== this.state.filter.value) {
                    delete this.params[filter]
                }
            }
            var filter = this.state.filter.value.split('/')
            filter = filter[filter.length-1]
            this.params[filter] = values;
        }
        this.fetch_page(1, true);
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

            // Generate query
            let query = this.gen_query(this.params);

            // Set URL
            this.props.history.push('/' + this.model + query);
            this.state.loading = true;

            // Fetch new grid model data
            fetch('/api/' + this.model + query, {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    this.state.page = json.page;
                    this.state.total_pages = json.total_pages;
                    this.state.models = json.results;
                    this.state.loading = false;
                    this.setState(this.state);
                });
        }
    }

    filter_toggle() {
        this.state.filterOpen = !this.state.filterOpen;
        this.setState(this.state);
    }

    sort_toggle() {
        this.state.sortOpen = !this.state.sortOpen;
        this.setState(this.state);
    }

    render() {
        var rows = []
        var no_results = ''
        if(this.state.models.length == 0 && !this.state.loading) {
            no_results = (
                <h1 style={{textAlign: 'center', margin: '20px'}}>
                    No Results
                </h1>
            );
        }
        for(var i = 0; i < this.state.models.length; i++) {
            var model = this.state.models[i];
            switch(this.props.name) {
                case "Games":
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
                        <ul className='model-attribute'>
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
                        <ul className='model-attribute'>
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

        // Filtering
        var filter_type = (
            <DropdownMenu>
                {filters[this.model].map(function(filter, i) {
                    return (
                        <DropdownItem key={i} onClick={() => {
                            if(this.state.filter !== filter) {
                                this.set_values('');
                            }
                            this.state.filter=filter;
                            this.setState(this.state)
                        }}>{filter.label}</DropdownItem> 
                    );
                }, this)}
            </DropdownMenu>
        );

        // Sorting
        var sort_type = (
            <DropdownMenu>
                {sorts[this.model].map(function(sort, i) {
                    return (
                        <DropdownItem key={i} onClick={() => {
                            this.state.sort=sort;
                            this.setState(this.state)
                            this.params['sort'] = this.state.sort.value
                            this.fetch_page(1, true);
                        }}>{sort.label}</DropdownItem> 
                    );
                }, this)}
            </DropdownMenu>
        );
        return (
            <div className="container">
                <div className='page-header'>
                    <Card>
                        <CardHeader>
                            <Row className="justify-content-md-center">
                                <h1>{this.props.name}</h1>
                            </Row>
                        </CardHeader>
                        <CardBody>
                            <Row className="justify-content-md-center">
                                <Col sm='auto'>
                                    <Dropdown isOpen={this.state.filterOpen} toggle={this.filter_toggle.bind(this)}>
                                        <DropdownToggle color='primary' caret>
                                            {this.state.filter.label}
                                        </DropdownToggle>
                                        {filter_type}
                                    </Dropdown>
                                </Col>
                                <Col sm='8'>
                                    <MultiSelect options={this.state.filter_options[this.state.filter.value]} name='' set_values={this.set_values.bind(this)} values={this.state.values} />
                                </Col>
                                <Col sm='auto'>
                                    <Dropdown isOpen={this.state.sortOpen} toggle={this.sort_toggle.bind(this)}>
                                        <DropdownToggle color='primary' caret>
                                            {this.state.sort.label}
                                        </DropdownToggle>
                                        {sort_type}
                                    </Dropdown>
                                </Col>
                            </Row>
                        </CardBody>
                    </Card>
                </div>
                <section>
                    <Row className="justify-content-md-center">
                    {this.state.models.map(function(model, i) {
                        return (
                                <Card key={i} className='grid-model'>
                                    <Link to={'/' + this.props.name.toLowerCase().slice(0, this.props.name.length - 1) + '/' + model.id}>
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
        );
    }

}
export default ModelGrid;
