const assert = require('assert');
const requirejs = require('requirejs');

requirejs.config({
  baseUrl: 'js',
  nodeRequire: require,
});

const util = requirejs('app/util');

describe('Util', () => {
  describe('#getCookie', () => {
    const tests = {
      'session_token=fd797261-5b801a482994; api_key="sumner@flume.live"': [
        'api_key', 'sumner@flume.live',
      ],
      'ae=t; s=n; am=google-maps; 5=2; w=w; u=-1; ak=-1; aq=-1; a=p; o=1': [
        'am', 'google-maps',
      ],
    };

    it('should parse the cookie string correctly', () => {
      for (const key of Object.keys(tests)) {
        const [cookieName, cookieValue] = tests[key];
        assert.equal(cookieValue, util.getCookie(cookieName, key));
      }
    });
  });
});
