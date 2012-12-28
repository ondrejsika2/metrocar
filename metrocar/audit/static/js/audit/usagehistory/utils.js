// Generated by CoffeeScript 1.3.1
(function() {
  var __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  define([], function() {
    var utils;
    return utils = {
      extractCategories: function(data) {
        var categories, entry, exclude, field, key, location, route, val, _i, _j, _k, _len, _len1, _len2, _ref, _ref1;
        exclude = ['added', 'event', 'location', 'odometer', 'timestamp', 'unit_id', 'user_id'];
        categories = {};
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          route = data[_i];
          _ref = route.entries;
          for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
            location = _ref[_j];
            _ref1 = location.entries;
            for (_k = 0, _len2 = _ref1.length; _k < _len2; _k++) {
              entry = _ref1[_k];
              for (field in entry) {
                val = entry[field];
                if (__indexOf.call(exclude, field) < 0) {
                  categories[field] = true;
                }
              }
            }
          }
        }
        return ((function() {
          var _results;
          _results = [];
          for (key in categories) {
            val = categories[key];
            _results.push(key);
          }
          return _results;
        })()).sort();
      },
      extractGraphData: function(data) {
        return utils._extractGraphData(data, utils.extractCategories(data));
      },
      _extractGraphData: function(data, categories) {
        var cat, entry, location, result, route, routeData, _i, _j, _k, _l, _len, _len1, _len2, _len3, _ref, _ref1;
        result = {};
        for (_i = 0, _len = categories.length; _i < _len; _i++) {
          cat = categories[_i];
          result[cat] = [];
          for (_j = 0, _len1 = data.length; _j < _len1; _j++) {
            route = data[_j];
            routeData = [];
            _ref = route.entries;
            for (_k = 0, _len2 = _ref.length; _k < _len2; _k++) {
              location = _ref[_k];
              _ref1 = location.entries;
              for (_l = 0, _len3 = _ref1.length; _l < _len3; _l++) {
                entry = _ref1[_l];
                routeData.push({
                  value: entry[cat] || 0,
                  timestamp: entry.timestamp
                });
              }
            }
            result[cat].push(routeData);
          }
        }
        return result;
      }
    };
  });

}).call(this);
