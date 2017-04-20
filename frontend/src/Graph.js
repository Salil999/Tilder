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
        <ForceGraphNode node={{ id: 'topic1', label: 'topic 1', radius: 10 }} fill="red" />
        <ForceGraphNode node={{ id: 'topic2', label: 'topic 2', radius: 10 }} fill="red" />
        <ForceGraphNode node={{ id: 'topic3', label: 'topic 3', radius: 10 }} fill="red" />
        <ForceGraphNode node={{ id: 'topic4', label: 'topic 4', radius: 10 }} fill="red" />
        <ForceGraphNode node={{ id: 'topic5', label: 'topic 5', radius: 10 }} fill="red" />
        <ForceGraphLink link={{ source: 'topic1', target: 'topic2', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic1', target: 'topic3', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic1', target: 'topic4', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic1', target: 'topic2', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic2', target: 'topic3', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic2', target: 'topic4', value: 2 }} />
        <ForceGraphLink link={{ source: 'topic3', target: 'topic5', value: 2 }} />
      </InteractiveForceGraph>
    );
  }
}

export default Graph;