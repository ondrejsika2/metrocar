// Generated by CoffeeScript 1.3.1
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __slice = [].slice;

  define(['backbone'], function(Backbone) {
    var Router;
    return Router = (function(_super) {

      __extends(Router, _super);

      Router.name = 'Router';

      function Router() {
        return Router.__super__.constructor.apply(this, arguments);
      }

      Router.prototype.routes = {
        'q/*query': 'query'
      };

      Router.prototype.query = function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      };

      return Router;

    })(Backbone.Router);
  });

}).call(this);
