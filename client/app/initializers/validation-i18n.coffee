`import Ember from 'ember'`
`import ValidationMessages from 'ember-validations/messages'`


Initializer =
  name: 'validation-i18n',
  after: 't',
  initialize: (container, application) ->

    t = container.lookup('utils:t');
    Ember.I18n = {};
    Ember.I18n.t = t;

    ValidationMessages.render = (attribute, context) ->

      error = Ember.I18n.t('errors.' + attribute, context)

      regex = new RegExp("{{(.*?)}}")
      attributeName = "";

      if regex.test(error)
        attributeName = regex.exec(error)[1];

      return error.replace(regex, context[attributeName])



`export default Initializer`
