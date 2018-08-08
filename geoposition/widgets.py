from __future__ import unicode_literals

import json

from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    template_name = 'geoposition/widgets/geoposition.html'

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def get_config(self):
        return {
            'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
            'map_options': json.dumps(settings.MAP_OPTIONS),
            'marker_options': json.dumps(settings.MARKER_OPTIONS),
        }

    def get_context(self, name, value, attrs):
        # Django 1.11 and up
        context = super(GeopositionWidget, self).get_context(
            name, value, attrs)
        context['latitude'] = {
            'widget': context['widget']['subwidgets'][0],
            'label': _("latitude"),
        }
        context['longitude'] = {
            'widget': context['widget']['subwidgets'][1],
            'label': _("longitude"),
        }
        context['config'] = self.get_config()
        return context

    def format_output(self, rendered_widgets):
        # Django 1.10 and down
        return render_to_string(
            'geoposition/widgets/geoposition.html', {
                'latitude': {
                    'html': rendered_widgets[0],
                    'label': _("latitude"),
                },
                'longitude': {
                    'html': rendered_widgets[1],
                    'label': _("longitude"),
                },
                'config': self.get_config(),
            })

    class Media:
        js = (
            '//unpkg.com/leaflet@1.3.3/dist/leaflet.js',
            '//unpkg.com/esri-leaflet@2.2.2/dist/esri-leaflet.js',
            '//unpkg.com/esri-leaflet-geocoder@2.2.13/dist/esri-leaflet-geocoder.js',
            'geoposition/geoposition.js',
        )
        css = {
            'all': (
                '//unpkg.com/leaflet@1.3.3/dist/leaflet.css',
                '//unpkg.com/esri-leaflet-geocoder@2.2.13/dist/esri-leaflet-geocoder.css',
                'geoposition/geoposition.css',
            )
        }
