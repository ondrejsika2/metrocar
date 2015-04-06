`import Ember from 'ember'`
`import config from './config/environment'`

Router = Ember.Router.extend
  location: config.locationType

Router.map ->
  @route 'layout'

  @route 'credentials', ->
    @route 'login'
    @route 'signup'

  @route 'reservations', ->
    @route 'list'
    @route 'create'
    @route 'browse-cars'

  @route 'fuelbill', ->
    @route 'list'
    @route 'create'

  @route 'profile'

  @route 'accountactivity', ->
    @route 'timeline'

`export default Router`
