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

from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource

from todolist.todo.models import Todo
from todolist.api.authorization import TodoAuthorization


class TodoResource(ModelResource):

    class Meta:
        queryset = Todo.objects.all()
        resource_name = 'todo'
        authorization = TodoAuthorization()
        authentication = ApiKeyAuthentication()

    def obj_create(self, bundle, **kwargs):
        """ A ORM-specific implementation of 'obj_create'.
            Assigns the user_id argument with the current authenticated user.
            The user_id is not required in API call.
        """
        kwargs['user_id'] = bundle.request.user.id
        return super(TodoResource, self).obj_create(bundle, **kwargs)
