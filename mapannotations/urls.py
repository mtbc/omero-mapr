#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>,
#
# Version: 1.0


from mapannotations import views
from django.conf.urls import url, patterns
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache

from map_settings import map_settings

reverse_lazy = lazy(reverse, str)

# concatenate aliases to use in url regex
MENU_MAPPER_REGEX = "(%s)" % ("|".join(map_settings.MENU_MAPPER))
DEFAULT_MENU = map_settings.MENU_MAPPER.iterkeys().next()


urlpatterns = patterns('',)

# alias
for m in map_settings.MENU_MAPPER:
    urlpatterns += (
        url(r'^(?i)%s/$' % m, views.index,
            {'menu': m},
            name="mapindex_%s" % m),
        )

urlpatterns += (

    # core
    url(r'^$', never_cache(
        RedirectView.as_view(
            url=reverse_lazy('mapindex_%s' % DEFAULT_MENU),
            permanent=True,
            query_string=True)),
        name="mapindex"),

    url(r'^api/experimenters/(?P<menu>%s)/'
        r'(?P<experimenter_id>([-1]|[0-9])+)/$' % MENU_MAPPER_REGEX,
        views.api_experimenter_detail,
        name='mapannotations_api_experimenter'),
    url(r'^api/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.api_mapannotation_list,
        name='mapannotations_api_mapannotations'),
    url(r'^api/plates/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.api_plate_list,
        name='mapannotations_api_plates'),
    url(r'^api/images/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.api_image_list,
        name='mapannotations_api_images'),

    url(r'^api/paths_to_object/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.api_paths_to_object,
        name='mapannotations_api_paths_to_object'),

    # TODO: c_id takes namedValue.name as an attribute, make sure regex match
    url(r'^metadata_details/(?P<c_type>%s)/'
        r'(?P<c_id>(.*))/$' % MENU_MAPPER_REGEX,
        views.load_metadata_details,
        name="mapannotations_load_metadata_details"),

    url(r'^api/annotations/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.api_annotations,
        name='mapannotations_api_annotations'),

    # autocomplete
    url(r'^autocomplete/(?P<menu>%s)/$' % MENU_MAPPER_REGEX,
        views.mapannotations_autocomplete,
        name='mapannotations_autocomplete'),

)
