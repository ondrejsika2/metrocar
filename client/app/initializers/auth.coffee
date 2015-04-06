`import Authenticator from 'client/app/pods/authenticators/custom-authenticator'`


Initializer =
  name:       'custom-auth',
  before:      'simple-auth',
  initialize: (container, application) ->

    application.register('authenticator:custom', Authenticator);
    application.inject('route','auth-custom', 'authenticator:custom');
    application.inject('controller','auth-custom', 'authenticator:custom');
    application.inject('adapter','session', 'simple-auth-session:main');



`export default Initializer`
