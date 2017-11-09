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
    'developer': 'dark',
    'event': 'primary'
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

    grab_words(words, offset, width=2*grab_radius) {
        if(words.length == 0) {
            return ''
        }
        width = Math.min(words.length, width)
        var contains_react = false
        for(var i = offset; i < offset + width; i++) {
            if(typeof words[i] !== 'string') {
                contains_react = true
                break
            }
        }
        var slice = words.slice(offset, offset + width)
        if(slice.length == 0 || slice == null) {
            return ''
        }
        if(contains_react) {
            return (
                <div>
                    {slice.map((t, i) => <span key={i}>{t}</span>)
                        .reduce((accu, elem) => {
                            return accu === null ? [elem] : [...accu, ' ', elem]
                        }, null)}
                </div>
            )
        } else {
            return slice.join(' ')
        }
    }

    highlight_word(words, word) {
        if(words == null) {
            return false
        }
        for(var i = 0; i < words.length; i++) {
            if(typeof words[i] === 'string'
                && words[i].toLowerCase().indexOf(word.toLowerCase()) != -1) {
                var idx = words[i].toLowerCase().indexOf(word.toLowerCase())
                words[i] = (
                    <span>
                        {words[i].substring(0, idx)}
                        <span style={{backgroundColor: 'yellow'}}>
                            {words[i].substring(idx, idx + word.length)}
                        </span>
                        {words[i].substring(idx + word.length, words[i].length)}
                    </span>
                )
                return true
            }
        }
        return false
    }

    assemble_words_list(list) {
        if(list == null) {
            return {found: false, text: ''}
        }
        for(var i = 0; i < list.length; i++) {
            list[i] = this.assemble_words(list[i]).text
        }
        return this.assemble_words(list, 7)
    }

    assemble_words(words, width=15) {
        if(words == null) {
            return {found: false, text: ''}
        }
        var idx = -1
        for(var i = 0; i < words.length; i++) {
            if(typeof words[i] !== 'string') {
                idx = i
                break
            }
        }

        var grabbed_words = this.grab_words(words, idx == -1 ? 0 : Math.max(idx - width, 0), 2 * width)
        return {found: idx != -1, text: idx != -1 ? (<span>{grabbed_words}</span>) : grabbed_words}
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
            let words = this.state.query.split('+')

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
                                    name: j.name.split(/\s+/),
                                    img: j.img,
                                    id: json.results[i].id,
                                    desc: '',
                                    alt_names: [],
                                    link: 'link' in j ? [j.link] : ('website' in j ? [j.website] : '')
                                }

                                instance.desc = j.desc == null ? '' : j.desc.replace(/<[^>]*>/g,' ')
                                var elem = document.createElement('textarea');
                                elem.innerHTML = instance.desc;
                                instance.desc = elem.value.split(/\s+/);

                                if('alt_names' in j) {
                                    for(var k = 0; k < j.alt_names.length; k++) {
                                        instance.alt_names[k] = j.alt_names[k].split(/\s+/)
                                    }
                                }

                                for(var k = 0; k < words.length; k++) {
                                    let word = words[k];
                                    while(this.highlight_word(instance.name, word));
                                    while(this.highlight_word(instance.desc, word));
                                    switch(json.results[i].type) {
                                        case "game":
                                            for(var l = 0; l < instance.alt_names.length; l++) {
                                                while(this.highlight_word(instance.alt_names[l], word));
                                            }
                                            break;
                                        case "developer":
                                        case "event":
                                            while(this.highlight_word(instance.link, word));
                                            break;
                                    }
                                }

                                instance.name = this.assemble_words(instance.name)
                                instance.desc = this.assemble_words(instance.desc)
                                instance.alt_names = this.assemble_words_list(instance.alt_names)
                                instance.link = this.assemble_words(instance.link)

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
            if(model.name.found || model.desc.found) {
                if(model.desc.text === '') {
                    rows.push(<p>No Description</p>)
                } else {
                    rows.push(<p>{model.desc.text}</p>)
                }
            } else if (model.alt_names.found) {
                rows.push(<p>{model.alt_names.text}</p>)
            } else if (model.link.found) {
                rows.push(<p>{model.link.text}</p>)
            } else {
                if(model.desc.text === '') {
                    rows.push(<p>No Description</p>)
                } else {
                    rows.push(<p>{model.desc.text}</p>)
                }
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
                                        <Col sm='10'>
                                            <Link to={'/' + model.type + '/' + model.id}>
                                                <h4><span className='align-middle'>{model.name.text}</span></h4>
                                            </Link>
                                        </Col>
                                        <Col className='text-right' sm='2'>
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
