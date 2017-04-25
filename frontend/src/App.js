import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import _ from 'lodash'

import Graph from './Graph'

class App extends Component {
  constructor(){
    super()

    this.updateResults = this.updateResults.bind(this)
  }
  
  state = {
    text: "",
    results: "",
    sentences: [],
    graph: {}
  }

  updateResults(res){
    return res
      .json()
      .then(d => this.setState({results: d.summary, sentences: d.sentences, graph: d.graph}))
      .then(() => {console.log(this.state)})
  }

  getData(){
    let nodes = []
    let edges = []

    // console.log(_(this.state.graph).mapKeys(_.identity).value())

    for(let key in this.state.graph){
      if(this.state.graph.hasOwnProperty(key)){
        console.log(this.state.graph[key])
      }
    }

    return ({
      nodes: [
        { id: 'topic1', label: 'topic 1'},
        { id: 'topic2', label: 'topic 2'},
        { id: 'topic3', label: 'topic 3'},
        { id: 'topic4', label: 'topic 4'},
        { id: 'topic5', label: 'topic 5'}
      ],
      edges: [
        {source: 'topic1', target: 'topic2'},
        {source: 'topic1', target: 'topic3'},
        {source: 'topic1', target: 'topic4'},
        {source: 'topic2', target: 'topic3'},
        {source: 'topic2', target: 'topic4'},
        {source: 'topic4', target: 'topic5'},
      ]
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
          <code>{this.state.results.split('\n').map(l => (<span key={l}>{l}<br /></span>))}</code>
        </p>
        <Graph data={this.getData()} />
      </div>
    );
  }
}

export default App;
