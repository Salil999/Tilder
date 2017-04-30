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
    wikipedia: "",
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
        nodes.push({
          id: key,
          label: key
        })
        this.state.graph[key]
          .forEach(s => {
            nodes.push({
              id: s,
              label: s
            })
            edges.push({
              source: key,
              target: s
            })
          })
      }
    }

    nodes = _.uniqBy(nodes, 'id')
    edges = _.uniqBy(edges, e => e.source+' - ' +e.target)

    return ({
      nodes,
      edges
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
          <input 
            value={this.state.wikipedia}
            onChange={e => this.setState({wikipedia: e.target.value})}
          />
          <br />
          <input type="submit" onClick={e => fetch(`http://localhost:5000/wiki/${this.state.wikipedia}`).then(this.updateResults).then(this.setState({wikipedia: ""}))}></input>
          <br />
          <pr />
          <br />
          <textarea value={this.state.text} onChange={e => this.setState({text: e.target.value})}></textarea>
          <br />
          <input type="submit" onClick={e => fetch(`http://localhost:5000/text`, {
            method: 'post',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.state.text)
          }).then(this.updateResults).then(this.setState({text: ""}))}></input>
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
