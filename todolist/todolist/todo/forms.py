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

""" Contains the form for the Todo model.
"""

from django.forms import ModelForm

from todolist.forms import BootstrapForm
from todolist.noconflict import classmaker
from todolist.todo.models import Todo


class TodoForm(BootstrapForm, ModelForm):
    __metaclass__ = classmaker()

    class Meta:
        model = Todo



