`import Ember from 'ember'`
`import config from './config/environment'`

Router = Ember.Router.extend
  location: config.locationType

Router.map ->
  @route 'layout'

  @route 'credentials', ->
    @route 'login'
    @route 'signup'
    @route 'success'

  @route 'reservations', ->
    @route 'list'
    @route 'create'

  @route 'fuelbill', ->
    @route 'list'
    @route 'create'

  @route 'profile', ->
    @route 'detail'
    @route 'success'
    @route 'changepassword'
    @route 'successpassword'

  @route 'accountactivity', ->
    @route 'timeline'

  @route 'forbidden', {path: '/forbidden'}
  @route 'error', {path: '/*path'}

`export default Router`
