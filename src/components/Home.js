import React from 'react'
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom'

class Home extends React.Component {
    
    constructor(props) {
        super(props);
        document.title = "Home - BGDB"; 
    }

    render() {
        return (
            <div class="container">
            <div id="main-carousel" class="carousel slide" data-ride="carousel">
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img class="d-block w-100" src="http://www.erzo.org/shannon/images-rpg/catan5-1.jpg" alt="First slide" height={600} style={{margin: '0 auto'}}/>
                        <div class="carousel-caption d-none d-md-block" style={{background: 'rgba(0,0,0,0.5)'}}>
                            <h3>Settlers of Catan</h3>
                            <p>Build your settlement and trade resources with friends only to find out they're your worst enemies</p>
                        </div>
                    </div>
                    <div class="carousel-item">
                        <img class="d-block w-100" src="https://i5.walmartimages.ca/images/Large/313/221/1313221.jpg?odnBound=460" alt="Second slide" height={600} style={{margin: '0 auto'}}/>
                        <div class="carousel-caption d-none d-md-block" style={{background: 'rgba(0,0,0,0.5)'}}>
                            <h3>Monopoly</h3>
                            <p>Tensions rise on the Boardwalk as you try to catch a runaway train and pass Go to escape rent</p>
                        </div>
                    </div>
                    <div class="carousel-item">
                        <img class="d-block w-100" src="https://fthmb.tqn.com/gPrPIWmEiMGtka1e1NjW9PFUN_M=/960x0/filters:no_upscale()/about/clue-58a6f5775f9b58a3c91a4cc5.jpg" alt="Third slide" height={600} style={{margin: '0 auto'}}/>
                        <div class="carousel-caption d-none d-md-block" style={{background: 'rgba(0,0,0,0.5)'}}>
                            <h3>Clue</h3>
                            <p>Unlock your inner Sherlock Holmes and solve the murder before it's too late</p>
                        </div>
                    </div>
                </div>
                <a class="carousel-control-prev" href="#main-carousel" role="button" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </a>
                <a class="carousel-control-next" href="#main-carousel" role="button" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </a>
            </div>
            </div>
        );
    }

}

export default Home;