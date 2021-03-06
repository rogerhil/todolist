# TodoList
# Copyright (C) 2013 Rogerio Hilbert Lima <rogerhil@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from todolist.views import Homepage

from todolist.todo.models import Todo
from todolist.api.resource import TodoResource

todo_resource = TodoResource()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Homepage.as_view(), name='home'),
    url(r'^tdauth/', include('todolist.tdauth.urls')),
    url(r'^todo/', include('todolist.todo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(todo_resource.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
)
