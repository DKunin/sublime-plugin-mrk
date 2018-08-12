'use strict';

const fetch = require('node-fetch');
const validUrl = require('valid-url');

let str = '';
let config;

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

    str.split('\n').forEach(function(singleLine) {
        if (validUrl.isUri(str)) {
            fetch(
                `https://wt-7c34bb748e3e4073b3f657c0ae1afac9-0.run.webtask.io/link-to-markdown?url=${str}`
            )
                .then(result => result.text())
                .then(result => {
                    process.stdout.write(result);
                });
        }
    });
});
