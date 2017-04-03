const fetch = require('node-fetch')

const baseURL = 'https://www.coursera.org/'

fetch(baseURL + '/api/onDemandLectureVideos.v1/bVgqTevEEeWvGQrWsIkLlw~7zA4L?includes=video&fields=onDemandVideos.v1(subtitlesTxt)')
  .then(r => r.json())
  .then(data => data.linked["onDemandVideos.v1"][0].subtitlesTxt.en)
  .then(subURL => fetch(baseURL + subURL))
  .then(r => r.text())
  .then(console.log)

