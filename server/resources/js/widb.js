/*
 * widb.js
 */

$(document).ready(() => {
    $('.log-panel-body').html('Hello world');
    let ws = new WebSocket('ws://localhost:8080/ws');
    ws.onopen = () => {
      console.log('gotHere');
    }
    ws.onmessage = () => {
        console.log('on Message');
    }
});
