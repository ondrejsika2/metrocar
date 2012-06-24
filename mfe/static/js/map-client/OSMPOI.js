/* based on OpenLayers.Format.Text */

/**
 * @requires OpenLayers/Feature/Vector.js
 * @requires OpenLayers/Geometry/Point.js
 */

/**
 * Class: OpenLayers.Format.OSMPOI
 * Read OSMPOI text format. Create a new instance with the <OpenLayers.Format.OSMPOI>
 *     constructor. This reads text which is formatted like CSV text, using
 *     spaces as the seperator by default.
 *
 * Inherits from:
 *  - <OpenLayers.Format>
 */
OpenLayers.Format.OSMPOI = OpenLayers.Class(OpenLayers.Format, {
    
    /**
     * APIProperty: defaultStyle
     * defaultStyle allows one to control the default styling of the features.
     *    It should be a symbolizer hash. By default, this is set to match the
     *    Layer.Text behavior, which is to use the default OpenLayers Icon.
     */
    defaultStyle: null,
     
    /**
     * Constructor: OpenLayers.Format.OSMPOI
     * Create a new parser for OSMPOI text.
     *
     * Parameters:
     * options - {Object} An optional object whose properties will be set on
     *     this instance.
     */
    initialize: function(options) {
        options = options || {};

        if(!options.defaultStyle) {
            options.defaultStyle = {
                'externalGraphic': OpenLayers.Util.getImagesLocation() + "marker.png",
                'graphicWidth': 21,
                'graphicHeight': 25,
                'graphicXOffset': -10.5,
                'graphicYOffset': -12.5
            };
        }
        
        OpenLayers.Format.prototype.initialize.apply(this, [options]);
    }, 

    /**
     * APIMethod: read
     * Return a list of features from a Space Seperated Values text string.
     * 
     * Parameters:
     * data - {String} 
     *
     * Returns:
     * An Array of <OpenLayers.Feature.Vector>s
     */
    read: function(text) {
        var lines = text.split('\n');
        var features = [];
        // length - 1 to allow for trailing new line
        for (var lcv = 0; lcv < (lines.length - 1); lcv++) {
            var currLine = lines[lcv].replace(/^\s*/,'').replace(/\s*$/,'');
        
            if (currLine.charAt(0) != '#') { /* not a comment */
               var vals = currLine.split(' ');
               var geometry = new OpenLayers.Geometry.Point(0,0);
               var attributes = {};
               var style = this.defaultStyle ? 
                   OpenLayers.Util.applyDefaults({}, this.defaultStyle) :
                   null;  
               var icon, iconSize, iconOffset, overflow;
               if (vals[0] && vals[1] && vals[2]) {
                   geometry.x = parseFloat(vals[0]);
                   geometry.y = parseFloat(vals[1]);
                   attributes['id'] = vals[2];
                   if (this.internalProjection && this.externalProjection) {
                       geometry.transform(this.externalProjection, 
                                          this.internalProjection); 
                   }
                   var feature = new OpenLayers.Feature.Vector(geometry, attributes, style);
                   features.push(feature);
               }
            }
        }
        return features;
    },   
    CLASS_NAME: "OpenLayers.Format.OSMPOI" 
});
