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
    Badge
} from 'reactstrap';

const badge = {
    'game': 'success',
    'genre': 'danger',
    'developers': 'dark',
    'events': 'primary'
};

const grab_radius = 15

class Search extends React.Component {

    constructor(props) {
        super(props)
        this.params = this.parse_query(props.location.search)
        this.params['per_page'] = 10;
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

    grab_words(text, width) {
        var words = text.split(/\s+/)
        return words.slice(0, width).join(' ') + (words.length > 30 ? '...' : '')
    }

    highlight_text(text, word, radius=grab_radius) {
        var words = text.split(/\s+/)
        var index = -1;
        var complete_word = ''
        for(var i = 0; i < words.length; i++) {
            if(words[i].toLowerCase().indexOf(word.toLowerCase()) != -1) {
                var idx = words[i].toLowerCase().indexOf(word.toLowerCase())
                complete_word = (
                    <span>
                        {words[i].substring(0, idx)}
                        <span style={{backgroundColor: 'yellow'}}>
                            {words[i].substring(idx, idx + word.length)}
                        </span>
                        {words[i].substring(idx + word.length, words[i].length)}
                    </span>
                )
                index = i;
                break;
            }
        }
        if(index == -1) {
            return -1
        }
        var b     = Math.max(index - radius, 0)
        var e     = Math.min(index + radius, words.length)
        var begin = Math.max(b - (radius - (e - index)), 0)
        var end   = Math.min(e + (radius - (index - b)), words.length)
        var before = begin == 0 ? '' : '...'
        var after = ''
        for(var i = begin; i < end; i++) {
            if(i < index) {
                before += words[i] + ' '
            }
            if(i > index) {
                after += ' ' + words[i]
            }
        }
        after += end == words.length ? '' : '...'
        return (
            <p>
                <span>{before}</span>
                {complete_word}
                <span>{after}</span>
            </p>
        );
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
            let words = this.state.query.split(/\s+/)

            // Fetch new grid model data
            fetch('/api/search' + query, {method: 'GET'})
                .then(response => response.json())
                .then(json => {
                    this.state.models = []
                    this.state.page = json.page;
                    this.state.total_pages = json.total_pages;
                    var models = {}
                    var count = 0;
                    for(let i = 0; i < json.results.length; i++) {
                        fetch('/api/' + json.results[i].type + 's/' + json.results[i].id, {method: 'GET'})
                            .then(r => r.json())
                            .then(j => {
                                var instance = {
                                    type: json.results[i].type,
                                    name: j.name,
                                    img: j.img,
                                    id: json.results[i].id,
                                    attributes: []
                                }
                                var raw_desc = j.desc == null ? '' : j.desc.replace(/<[^>]*>/g,' ')
                                var elem = document.createElement('textarea');
                                elem.innerHTML = raw_desc;
                                raw_desc = elem.value;
                                instance['desc'] = this.grab_words(raw_desc, 0, 2 * grab_radius)
                                for(var k = 0; k < words.length; k++) {
                                    let word = words[k];
                                    let desc_highlight = this.highlight_text(raw_desc, word);
                                    if(desc_highlight != -1) {
                                        instance.attributes.push(desc_highlight)
                                    }
                                    switch(json.results[i].type) {
                                        case "game":
                                            //alt_names
                                            break;
                                        case "developer":
                                            //website
                                            break;
                                        case "event":
                                            //link
                                            break;
                                    }
                                }
                                models[i] = instance
                                count += 1
                                if(count == json.results.length) {
                                    for(var k = 0; k < json.results.length; k++) {
                                        this.state.models.push(models[k])
                                    }
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
            if(model.attributes.length == 0) {
                rows.push(<p>{model.desc}</p>)
            } else {
                rows.push(model.attributes.map(function(context, i) {
                    return <p key={i}>{context}</p>
                }));
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
                            <Col key={i} sm='12'>
                                <Card className='search-model'>
                                    <CardHeader>
                                        <Row>
                                        <Col>
                                            <Link to={'/' + model.type + '/' + model.id}>
                                                <h4><span className='align-middle'>{model.name}</span></h4>
                                            </Link>
                                        </Col>
                                        <Col className='text-right'>
                                            <Link to={'/' + model.type + 's'}>
                                                <Badge style={{textAlign: 'right'}} color={badge[model.type]}><h4>{model.type}</h4></Badge>
                                            </Link>
                                        </Col>
                                        </Row>
                                    </CardHeader>
                                    <CardBody className='search-model-text'>
                                        {rows[i]}
                                    </CardBody>
                                </Card>
                            </Col>
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
