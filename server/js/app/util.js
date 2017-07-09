/*
 * @fileoverview Utility functions for the Wireless Debugging web app.
 */

define([], () => {
  /**
   * Gets the cookie value for the given cookie name.
   *
   * @param {string} key the cookie name to retrieve
   * @param {string} cookieString=document.cookie the cookie string to use for
   *     parsing (this is primarily for testing purposes)
   * @returns {string} the cookie value
   */
  function getCookie(key, cookieString = document.cookie) {
    // Extract the cookie value from the cookies on the web page.
    const cookieStrings = cookieString.replace(/['"]+/g, '').split(';');
    for (let i = 0; i < cookieStrings.length; i++) {
      const [cookieKey, cookieValue] = cookieStrings[i].trim().split('=');
      if (cookieKey === key) {
        return cookieValue;
      }
    }

    return null;
  }

  return {
    getCookie: getCookie,
  };
});
