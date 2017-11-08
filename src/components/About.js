import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'

class About extends React.Component {

    constructor(props) {
        super(props);
        document.title = "About - BGDB";
        this.state = {
            'Quangmire': [0,0,0],
            'anuragbakshi': [0,0,0],
            'jsphyin': [0,0,4],
            'aytiel': [0,0,15],
            'KLedet': [0,0,0],
            total: [0,0,19]
        };
        this.trello = {
            '53e2bdcf2041ed5793869e18': 'Quangmire',
            '52b512661a8b5aaf35003276': 'anuragbakshi',
            '58589311a6d8eef22a13c76d': 'jsphyin',
            '596ba9b2870eed3c04b7781e': 'aytiel',
            '58d172575c1863c115c95146': 'KLedet'
        }
        fetch('https://api.github.com/repos/jsphyin/idb/contributors', {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                for(var i = 0; i < json.length; i++) {
                    this.state[json[i]['login']][0] = json[i]['contributions'];
                    this.state.total[0] += json[i]['contributions'];
                }
                this.setState(this.state);
            });
        fetch('https://api.trello.com/1/board/EIE23URq/cards?key=08a3dc10723149d7a4ae84358b891ccd&token=429171254d122b908ec39035216d699feb5014c5c8df2bcd9fbb2ec1ba797167', {method: 'GET'})
            .then(response => response.json())
            .then(json => {
                for(var i = 0; i < json.length; i++) {
                    for(var j = 0; j < json[i]['idMembers'].length; j++) {
                        this.state[this.trello[json[i]['idMembers'][j]]][1] += 1;
                    }
                    this.state.total[1] += 1
                }
                this.setState(this.state);
            });
    }

    render() {
        const page_header = {
            paddingTop: '20px'
        }
        const about_person = {
            textAlign: 'center',
            margin: '20px'
        };
        const about_person_img = {
            width: '200px',
            height: '200px',
        };
        const about_person_name = {
            fontWeight: 'bold'
        };
        const about_person_detail = {
            textAlign: 'left'
        };
        return (
            <div class="container">
                <div id="about-site-header" style={page_header}>
                  <h2>The Site</h2>
                </div>
                <section id="about-site-content">
                    Board Game DB is a website for board game fans to search for games, genres, publishers, and events.
                </section>


                <div id="about-team-header" style={page_header}>
                    <h2>The Team - Board Gamers</h2>
                </div>
                <section id="about-team-content">
                    <div class="row">
                        <div class="col" style={about_person}>
                            <div class="row">
                                <div class="col">
                                  <img style={about_person_img} src="https://anuragbakshi.github.io/CS-373-Blog/assets/headshot.jpg"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <span style={about_person_name}>Anurag Bakshi</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <ul style={about_person_detail}>
                                        <li><strong>Bio:</strong> Anurag is a junior studying CS and Math at UT Austin. He enjoys traveling, road trips, and barbecue.</li>
                                        <li><strong>Responsibilities:</strong> Frontend, Backend, GCP and domain management</li>
                                        <li><strong>No. Of Commits:</strong> {this.state['anuragbakshi'][0]}</li>
                                        <li><strong>No. Of Issues:</strong> {this.state['anuragbakshi'][1]}</li>
                                        <li><strong>No. Of Unit Tests:</strong> {this.state['anuragbakshi'][2]}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="col" style={about_person}>
                            <div class="row">
                                <div class="col">
                                  <img style={about_person_img} src="https://quangmire.files.wordpress.com/2017/09/me.png"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <span style={about_person_name}>Quang Duong</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <ul style={about_person_detail}>
                                        <li><strong>Bio:</strong> Quang is a third year CS/Math student with an addiction to reading anything from fantasy to romance.</li>
                                        <li><strong>Responsibilities:</strong> Frontend, scraping and parsing data, Report</li>
                                        <li><strong>No. Of Commits:</strong> {this.state['Quangmire'][0]}</li>
                                        <li><strong>No. Of Issues:</strong> {this.state['Quangmire'][1]}</li>
                                        <li><strong>No. Of Unit Tests:</strong> {this.state['Quangmire'][2]}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="col" style={about_person}>
                            <div class="row">
                                <div class="col">
                                  <img style={about_person_img} src="https://jsphyinswe.files.wordpress.com/2017/09/headshot.jpg?w=300&h=300"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <span style={about_person_name}>Joseph Yin</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <ul style={about_person_detail}>
                                        <li><strong>Bio:</strong> Joseph is a third year student at UT pursuing a BS in computer science. In his free time he enjoys reading manga, browsing memes, and playing league.</li>
                                        <li><strong>Responsibilities:</strong> Task management, Frontend</li>
                                        <li><strong>No. Of Commits:</strong> {this.state['jsphyin'][0]}</li>
                                        <li><strong>No. Of Issues:</strong> {this.state['jsphyin'][1]}</li>
                                        <li><strong>No. Of Unit Tests:</strong> {this.state['jsphyin'][2]}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col" style={about_person}>
                            <div class="row">
                                <div class="col">
                                  <img style={about_person_img} src="https://kamronledet.files.wordpress.com/2017/09/15289202_897036407098184_508436949144464272_o.jpg"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <span style={about_person_name}>Kamron Ledet</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <ul style={about_person_detail}>
                                        <li><strong>Bio:</strong> Kamron Ledet is a third-year Computer Science major interested in programming for games and software. He also takes an interest in acting and has been active in theatre since junior high.</li>
                                        <li><strong>Responsibilities:</strong> Apiary, Domain management</li>
                                        <li><strong>No. Of Commits:</strong> {this.state['KLedet'][0]}</li>
                                        <li><strong>No. Of Issues:</strong> {this.state['KLedet'][1]}</li>
                                        <li><strong>No. Of Unit Tests:</strong> {this.state['KLedet'][2]}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="col" style={about_person}>
                            <div class="row">
                                <div class="col">
                                  <img style={about_person_img} src="https://aytiel.files.wordpress.com/2017/01/cropped-img_20160920_19234311.jpg?w=640"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <span style={about_person_name}>Alexander Lo</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <ul style={about_person_detail}>
                                        <li><strong>Bio:</strong> Alex is a third year computer science major with an interest in pursuing game and graphical development.</li>
                                        <li><strong>Responsibilities:</strong> Apiary, Frontend</li>
                                        <li><strong>No. Of Commits:</strong> {this.state['aytiel'][0]}</li>
                                        <li><strong>No. Of Issues:</strong> {this.state['aytiel'][1]}</li>
                                        <li><strong>No. Of Unit Tests:</strong> {this.state['aytiel'][2]}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <div id="about-stats-header" class="page-header">
                  <h2>Stats</h2>
                </div>
                <section id="about-stats-content">
                    <ul>
                        <li><strong>Total No. of Commits:</strong> {this.state.total[0]}</li>
                        <li><strong>Total No. of Issues:</strong> {this.state.total[1]}</li>
                        <li><strong>Total No. of Unit Tests:</strong> {this.state.total[2]}</li>
                        <li><a href="http://docs.boardgamedb.apiary.io/"><strong>Apiary</strong></a></li>
                        <li><a href="https://github.com/jsphyin/idb"><strong>Github</strong></a></li>
                        <li><a href="https://trello.com/b/EIE23URq/swe-project"><strong>Trello</strong></a></li>
                    </ul>
                </section>

                <div id="about-data-header" class="page-header">
                  <h2>Data</h2>
                </div>
                <section id="about-data-content">
                    <ul>
                        <li><a href="http://www.boardgamegeek.com/xmlapi">http://www.boardgamegeek.com/xmlapi</a></li>
                        <li><a href="http://www.mediawiki.org/wiki/API ">http://www.mediawiki.org/wiki/API </a></li>
                        <li><a href="http://www.reddit.com/dev/api">http://www.reddit.com/dev/api</a></li>
                        <li><a href="http://api.meetup.com">http://api.meetup.com</a></li>
                    </ul>
                    Using the Python <a href="http://docs.python-requests.org/en/master/">requests</a> library, we grabbed all the XML by iterating through all possible ids and filtering out all the non-board game items.
                </section>

                <div id="about-tools-header" class="page-header">
                  <h2>Tools</h2>
                </div>
                <section id="about-tools-content">
                    <ul>
                        <li><a href="https://github.com/"><strong>Github:</strong></a> We used Github as our version control system and to collaborate within our group.</li>
                        <li><a href="https://trello.com/"><strong>Trello:</strong></a> We used Trello to manage and delegate tasks for this project.</li>
                        <li><a href="https://apiary.io/"><strong>Apiary:</strong></a> We used Apiary to document our API endoints and responses.</li>
                        <li><a href="http://jinja.pocoo.org/"><strong>Jinja2:</strong></a> We used Jinja2 to reuse the layouts of common pages and dynamically generate parts of the webpage.</li>
                        <li><a href="http://flask.pocoo.org/"><strong>Flask:</strong></a> We used Flask as a lightweight Python web framework.</li>
                        <li><a href="http://getbootstrap.com/"><strong>Bootstrap:</strong></a> We used Bootstrap for the layout and style of our website.</li>
                        <li><a href="http://python-requests.org/"><strong>Requests:</strong></a> We used Requests to scrape data for our website.</li>
                    </ul>
                </section>

                <div id="about-report-header" class="page-header">
                  <h2><a href="https://utexas.app.box.com/v/boardgamedbreport">Report</a></h2>
                </div>
            </div>
        );
    }
}

export default About;
