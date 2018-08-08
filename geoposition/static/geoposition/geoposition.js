if (jQuery != undefined) {
  var django = {
    jQuery: jQuery,
  };
}

(function($) {
  $(document).ready(function() {
    try {
      var _ = L;
    } catch (ReferenceError) {
      console.log(
        'geoposition: "L" not defined.  You might not be connected to the internet.',
      );
      return;
    }

    $('.geoposition-widget').each(function() {
      var $container = $(this),
        $mapContainer = $('<div class="geoposition-map" />'),
        $latitudeField = $container.find('input.geoposition:eq(0)'),
        $longitudeField = $container.find('input.geoposition:eq(1)'),
        latitude = parseFloat($latitudeField.val()) || null,
        longitude = parseFloat($longitudeField.val()) || null,
        map,
        marker;

      $mapContainer.css(
        'height',
        $container.attr('data-map-widget-height') + 'px',
      );

      $container.append($mapContainer);

      map = L.map($mapContainer.get(0));

      L.tileLayer(
        'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
      ).addTo(map);

      var searchControl = L.esri.Geocoding.geosearch({
        useMapBounds: false,
      }).addTo(map);

      var results = L.layerGroup().addTo(map);

      if (latitude !== null && longitude !== null) {
        var latlng = [latitude, longitude];
        map.setView(latlng, 15);
        results.addLayer(L.marker(latlng));
      } else {
        map.setView([0, 0], 1);
      }

      searchControl.on('results', function(data) {
        results.clearLayers();
        for (var i = data.results.length - 1; i >= 0; i--) {
          var latlng = data.results[i].latlng;
          console.log(latlng);
          $latitudeField.val(latlng.lat);
          $longitudeField.val(latlng.lng);
          results.addLayer(L.marker(latlng));
        }
      });
    });
  });
})(django.jQuery);
