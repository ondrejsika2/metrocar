// Generated by CoffeeScript 1.3.1
(function() {
  var max, min;

  min = Math.min, max = Math.max;

  define({
    boundsToPolygon: function(_arg) {
      var bottom, left, right, top;
      left = _arg.left, right = _arg.right, top = _arg.top, bottom = _arg.bottom;
      return [[left, top], [right, top], [right, bottom], [left, bottom], [left, top]];
    },
    polygonToBounds: function(polygon) {
      var lat, lats, lon, lons;
      lats = (function() {
        var _i, _len, _ref, _results;
        _results = [];
        for (_i = 0, _len = polygon.length; _i < _len; _i++) {
          _ref = polygon[_i], lon = _ref[0], lat = _ref[1];
          _results.push(lat);
        }
        return _results;
      })();
      lons = (function() {
        var _i, _len, _ref, _results;
        _results = [];
        for (_i = 0, _len = polygon.length; _i < _len; _i++) {
          _ref = polygon[_i], lon = _ref[0], lat = _ref[1];
          _results.push(lon);
        }
        return _results;
      })();
      return {
        left: min.apply(null, lons),
        right: max.apply(null, lons),
        bottom: min.apply(null, lats),
        top: max.apply(null, lats)
      };
    },
    OLTransformLocationTypeFactory: function(type, from, to) {
      return function(_arg) {
        var lat, lon, obj;
        lon = _arg[0], lat = _arg[1];
        obj = new type(lon, lat);
        obj.transform(from, to);
        return obj;
      };
    }
  });

}).call(this);
