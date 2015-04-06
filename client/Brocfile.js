/* global require, module */

var EmberApp = require('ember-cli/lib/broccoli/ember-app');

var app = new EmberApp({
  name: 'client/app',

  lessOptions: {
    paths: [
      'bower_components/bootstrap/less'
    ]
  },
  'ember-bootstrap-datetimepicker': {
    "importBootstrapCSS": true,
    "importBootstrapJS": true,
    "importBootstrapTheme": true
  },

  outputPaths: {
    app: {
      html: 'index.html',
      css: {
        'app': '/assets/client.css'
      },
      js: '/assets/client.js'
    }
  }

});

app.import('bower_components/bootstrap/dist/js/bootstrap.js');
app.import('bower_components/metisMenu/dist/metisMenu.js');
app.import('bower_components/select2-bootstrap-css/select2-bootstrap.css');

app.import('bower_components/moment/locale/cs.js');

// Use `app.import` to add additional libraries to the generated
// output files.
//
// If you need to use different assets in different
// environments, specify an object as the first parameter. That
// object's keys should be the environment name and the values
// should be the asset to use in that environment.
//
// If the library that you are including contains AMD or ES6
// modules that you would like to import into your application
// please specify an object with the list of modules as keys
// along with the exports of each module as its value.

module.exports = app.toTree();
