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

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.Listing.as_view(), name='todo_listing'),
    url(r'^reload/$', views.ReloadListing.as_view(),
        name='todo_listing_relaod'),
    url(r'^add/$', views.Add.as_view(), name='todo_add'),
    url(r'^delete/(?P<pk>\d+)/$', views.Delete.as_view(), name='todo_delete'),
    url(r'^change/(?P<pk>\d+)/$', views.Change.as_view(), name='todo_change'),
    url(r'^change/(?P<pk>\d+)/mark_as_done/$', views.MarkAsDone.as_view(),
        name='todo_mark_done'),
    url(r'^change/(?P<pk>\d+)/priority/$', views.ChangePriority.as_view(),
        name='todo_change_priority'),
    url(r'^change/(?P<pk>\d+)/due_date/$', views.ChangeDueDate.as_view(),
        name='todo_change_due_date'),
    url(r'^change/(?P<pk>\d+)/description/$', views.ChangeDescription.as_view(),
        name='todo_change_description')
)
