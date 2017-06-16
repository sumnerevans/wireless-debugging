/*
 * @fileoverview (<>)
 */

define([], () => {
  function getCookie(key, cookieString = document.cookie) {
    // Extract the api key from the cookies on the web page.
    let cookieStrings = cookieString.replace(/['"]+/g, '').split(';');
    for (let i = 0; i < cookieStrings.length; i++) {
      let [cookieKey, cookieValue] = cookieStrings[i].trim().split('=');
      if (cookieKey === key) {
        return cookieValue;
      }
    }
  }

  return {
    getCookie: getCookie,
  };
});
