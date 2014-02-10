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

from tastypie.authorization import DjangoAuthorization


class TodoAuthorization(DjangoAuthorization):

    def read_list(self, object_list, bundle):
        qs = super(TodoAuthorization, self).read_list(object_list, bundle)
        return qs.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        r = super(TodoAuthorization, self).read_detail(object_list, bundle)
        return r and bundle.obj.user == bundle.request.user

    def create_detail(self, object_list, bundle):
        r = super(TodoAuthorization, self).create_detail(object_list, bundle)
        return r and bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        qs = super(TodoAuthorization, self).update_list(object_list, bundle)
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in qs:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        r = super(TodoAuthorization, self).update_detail(object_list, bundle)
        return r and bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        qs = super(TodoAuthorization, self).delete_list(object_list, bundle)
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in qs:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        r = super(TodoAuthorization, self).delete_detail(object_list, bundle)
        return r and bundle.obj.user == bundle.request.user
