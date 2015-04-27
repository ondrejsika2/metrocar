/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'client/app',
    podModulePrefix: 'client/app/pods',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',

    //'simple-auth': {
    //  authorizer: 'authorizer:custom'
    //},

    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
      defaultLocale: 'cs'
    },

    contentSecurityPolicy : {
      'default-src': "'none'",
      'script-src': "'self' 'unsafe-eval' *.googleapis.com maps.gstatic.com",
      'font-src': "'self' fonts.gstatic.com",
      'connect-src': "'self' maps.gstatic.com server.metrocar.knaisl.cz local.server.metrocar.dev",
      'img-src': "'self' *.googleapis.com maps.gstatic.com csi.gstatic.com www.gravatar.com",
      'style-src': "'self' 'unsafe-inline' fonts.googleapis.com maps.gstatic.com"
    },



  };

  if (environment === 'development') {
    //ENV.APP.LOG_RESOLVER = true;
    //ENV.APP.LOG_ACTIVE_GENERATION = true;
    //ENV.APP.LOG_TRANSITIONS = true;
    //ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    //ENV.APP.LOG_VIEW_LOOKUPS = true;

    ENV['metrocarServer'] = 'http://local.server.metrocar.dev';
    ENV['simple-auth'] = {
      serverTokenEndpoint: 'http://local.server.metrocar.dev/api/v1/auth-token/',
        crossOriginWhitelist: ['local.server.metrocar.dev'],
        store: 'simple-auth-session-store:local-storage'
    };

  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

    ENV['metrocarServer'] = 'http://server.metrocar.knaisl.cz';
    ENV['simple-auth'] = {
      serverTokenEndpoint: 'http://server.metrocar.knaisl.cz/api/v1/auth-token/',
      crossOriginWhitelist: ['server.metrocar.knaisl.cz'],
      store: 'simple-auth-session-store:local-storage'
    };

  }

  return ENV;
};
