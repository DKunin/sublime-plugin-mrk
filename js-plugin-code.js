'use strict';

const fetch = require('node-fetch');
const validUrl = require('valid-url');
const OgParser = require('open-graph-parser-function');

let str = '';
let config;

function processResult(openGraph, url) {
  return `- [${openGraph.title}](${url}) ![image](${openGraph.image}) ${openGraph.description}`;
}

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(data) {
    str += data;
});

process.stdin.on('end', function() {
    try {
        config = JSON.parse(process.argv[2]);
    } catch (e) {
        console.log(e);
        config = null;
    }

    str.split('\n').forEach(function(url) {
        if (validUrl.isUri(url)) {
            OgParser({ query: { url }}, function(error, data) {
                process.stdout.write(processResult(data, url) + '\n');
            });
        }
    });
});
