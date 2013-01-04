metrocar.maps
=============

This application contains :doc:`JavaScript <howto/js>` components for displaying and manipulating maps.

The map interface
-----------------
This is a specification of an mapping component.

* It should be require.js module that exports and object with a ``createMap`` function.

* ``createMap`` should accept one argument -- a DOM element on which the map should be created.

* It should return an object that provides an `API` for controlling the created map.

* The `API` should provide the following methods:


  * ``onMoved: (callback) ->``

    Calls `callback` when the map is moved.


  * ``getBounds: ->``

    Returns current bounds of what is visible on the map.

  	The result should be an object: ``{left, bottom, right, top}``


  * ``setBounds: ({left, bottom, right, top}) ->``

    Sets the map's viewpoint to given bounds


  * ``drawRoute: (route) ->``

    Draws a route (line) on the map.

  	The `route` argument should be an array of points, where each point looks like this: ``[longitude, latitude]``


  * ``drawMarker: ({location, content}) ->``

    Draws a marker on the map on given `location` (``[x, y]``).

  	If `content` is given, it will be displayed in a popup when user hovers over the marker.


  * ``drawIconMarker: ({location, content, icon, size, offset}) ->``

    Draws a marker with a specific image.

    Same as ``drawMarker``, except the image with URL given as `icon` is drawn instead of a generic marker. The `offset` parameter specifies the offset of the images top left corner from the actual `location`.


  * ``clear: ->``

    Clears all markers and routes from the map.


  * ``focus: (locations) ->``

    Setup the map view so that all `locations` are visible.


Implementations
---------------
There is an available implementation of this interface using OpenLayers.

To use it in your module, do::

	define ['maps/ol'], (OLMap) -> ...

