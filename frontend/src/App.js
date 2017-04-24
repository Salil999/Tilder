import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import Graph from './Graph'

class App extends Component {
  constructor(){
    super()

    this.updateResults = this.updateResults.bind(this)
  }
  
  state = {
    text: "",
    results: ""
  }

  updateResults(res){
    res.text()
      .then(d => this.setState({results: d}))
  }

  getData(){
    return ({
      topic1: ['topic2', 'topic3', 'topic4'],
      topic2: ['topic3', 'topic4'],
      topic3: ['topic5'],
    })
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to Tilder</h2>
        </div>
        <p className="App-intro">
          <textarea value={this.state.text} onChange={e => this.setState({text: e.target.value})}></textarea>
          <br />
          <input type="submit" onClick={e => fetch(`http://localhost:5000/text/${this.state.text}`).then(this.updateResults).then(this.setState({text: ""}))}></input>
          <br />
          <br />
          <br />
          <code>{this.state.results.split('\n').map(l => (<span>{l}<br /></span>))}</code>
        </p>
        <Graph data={this.getData()} />
      </div>
    );
  }
}

export default App;
