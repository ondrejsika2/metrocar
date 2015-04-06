`import DS from 'ember-data'`

Model = DS.Model.extend

  color: DS.attr('string')

  cars: DS.hasMany('car')

`export default Model`
