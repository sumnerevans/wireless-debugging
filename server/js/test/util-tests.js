let assert = require('assert');
let Browser = require('zombie');
let requirejs = require('requirejs');
const browser = new Browser();

requirejs.config({
  baseUrl: 'js',
  nodeRequire: require,
});

let util = requirejs('app/util');

describe('Util', () => {
  describe('#getCookie', () => {
    let tests = {
      'session_token=fd797261-c619-4291-bad6-5b801a482994; api_key="sumner@flume.live"': [
        'api_key', 'sumner@flume.live'
      ],
      'ae=t; s=n; am=google-maps; 5=2; aj=m; n=1; w=w; u=-1; ak=-1; aq=-1; a=p; o=1': [
        'am', 'google-maps'
      ],
    };

    it('should get the correct cookie from the document', () => {
      for (let key of Object.keys(tests)) {
        let [cookieName, cookieValue] = tests[key];
        assert.equal(cookieValue, util.getCookie(cookieName, key));
      }
    });
  });
});
