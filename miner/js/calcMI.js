#!/usr/bin/env node
const fs = require('fs')
const Promise = require('promise')
const _ = require('lodash')
const argv = require('yargs').argv;

const readFile = Promise.denodeify(fs.readFile);

// const SEG_SIZE = 300
const NUM_SEGS = 42

const makeHash = text => {
  let hash = {}

  _(text
    .split(' '))
    .map(w => w.toLowerCase())
    .map(w => [_.first((w.match(/[\w-']+/) || [''])[0].split('\'')), _.last((w.match(/[\w-']+/) || [''])[0].split('\''))])
    .map(_.uniq)
    .flatten()
    .value()

    // remove punct here
    .forEach((word, i) => {
      hash[word] = hash[word] || [];
      hash[word].push(i)
    })
    return hash

}

const getPhraseInstances = (phrase, hash) => {
  const startWord = _.first(phrase.split(' '))

  const startingPosition = 
    _(phrase)
      .split(' ')
      .map(word => hash[word])
      .tail()
      .value()

  // console.error(startWord, hash[startWord], startingPosition)

  return hash[startWord]
    .filter(pos => startingPosition.reduce((p, c, i) => p ? _.includes(c, pos+i+1) : p, true))
                  // pos + 1 exist in startPositon[0]
                  // pos + 2 exist in startPositon[1]
                  // ...
                  // pos + n exist in startPositon[n-1]

}

const getProbability = (inst1, inst2, size) => {

  const SEG_SIZE = Math.floor(size / NUM_SEGS);
  const numSegs = Math.ceil(size / SEG_SIZE);

  let numSegsWith1 = 0
  let numSegsWith2 = 0
  let numSegsWith1And2 = 0
  for(let i = 0; i < size; i+=SEG_SIZE){
    if(inst1.filter(pos => pos >= i && pos < i+SEG_SIZE).length > 0)               // could show up twice
      numSegsWith1 += 1
    if(inst2.filter(pos => pos >= i && pos < i+SEG_SIZE).length > 0)               // could show up twice
      numSegsWith2 += 1
    if(inst1.filter(pos => pos >= i && pos < i+SEG_SIZE).length > 0 && inst2.filter(pos => pos >= i && pos < i+SEG_SIZE).length > 0)               // could show up twice
      numSegsWith1And2 += 1
  }

  console.error(numSegsWith1, numSegsWith2, numSegsWith1And2, numSegs)

  return {
    prob1: (numSegsWith1+0.5)/(numSegs+1),
    prob2: (numSegsWith2+0.5)/(numSegs+1),
    prob1And2: (numSegsWith1And2+0.25)/(numSegs+1)
  }
    // inst1
      // .map()
}

const mi = (prob1, prob2, prob1And2) => {
  const probNot1 = 1 - prob1
  const probNot2 = 1 - prob2
  const prob1AndNot2 = prob1 - prob1And2
  const prob2AndNot1 = prob2 - prob1And2
  const probNot1AndNot2 = 1 - prob1AndNot2 - prob2AndNot1 - prob1And2

  const first = probNot1AndNot2 * Math.log2(probNot1AndNot2/(probNot1*probNot2))
  const second = prob2AndNot1 * Math.log2(prob2AndNot1/(probNot1*prob2))
  const third = prob1AndNot2 * Math.log2(prob1AndNot2/(probNot2*prob1))
  const fourth = prob1And2 * Math.log2(prob1And2/(prob1*prob2))

  return first + second + third + fourth
}

let _parsedHash = null;
let _firstPhraseInstances = []
let _secondPhraseInstances = []
let _documentSize = null;
readFile('../input.txt', 'utf-8')
  .then(makeHash)
  .then(hash => _parsedHash = hash)
  .then(() => _documentSize = _.max(_.map(_parsedHash, _.max)))
  .then(() => getPhraseInstances(argv.phrase1, _parsedHash))
  .then(instances => _firstPhraseInstances = instances)
  .then(() => getPhraseInstances(argv.phrase2, _parsedHash))
  .then(instances => _secondPhraseInstances = instances)
  .then(() => getProbability(_firstPhraseInstances, _secondPhraseInstances, _documentSize))
  .then(probs => mi(probs.prob1, probs.prob2, probs.prob1And2))
  .then(console.log)
  .catch(console.error)