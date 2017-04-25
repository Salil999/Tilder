import React, { Component } from 'react';
import {InteractiveForceGraph, ForceGraphNode, ForceGraphLink} from 'react-vis-force';

class Graph extends Component {
  render() {
    return (
      <InteractiveForceGraph 
        simulationOptions={{ height: 300, width: 300 }}
        labelAttr="label"
        onSelectNode={(node) => console.log(node)}
        highlightDependencies
        >
        {
          this.props.data.nodes.map(n => <ForceGraphNode key={n.id} node={{ ...n, radius: 10 }} fill="red" />)
        }
        {
          this.props.data.edges.map(e => <ForceGraphLink key={`${e.source} ${e.target}`} link={{ ...e, value: 2 }} />)
        }
      </InteractiveForceGraph>
    );
  }
}

export default Graph;