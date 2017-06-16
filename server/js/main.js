/*
 * @fileoverview This is the root Wireless Debug JavaScript file. It configures
 * requirejs.
 */

requirejs.config({
  'baseUrl': 'js',
  'paths': {
    'jquery': '//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.0/jquery.min',
    'bootstrap': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min',
    'chart': '//cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.bundle.min',
    'datatables': '//cdn.datatables.net/v/bs/dt-1.10.15/datatables.min',
  },
});

requirejs(['app/wireless-debug', 'jquery'], (WirelessDebug, $) => {
  // Run the Application
  $(document).ready(() => new WirelessDebug().start());
});
