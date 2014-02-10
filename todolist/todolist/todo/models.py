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

""" Contains the Todo model
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from todolist.utils import Choices


class Todo(models.Model):
    """ The Todo model.
    """

    class Priority(Choices):
        low = 1
        medium = 2
        high = 3

    class Status(Choices):
        todo = 'todo'
        done = 'done'
        expired = 'expired'

    description = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=Priority.choices(),
                                   default=Priority.low)
    status = models.CharField(max_length=32, choices=Status.choices(),
                              default=Status.todo, editable=False)
    user = models.ForeignKey(User, editable=False)

    def __unicode__(self):
        return unicode(self.description)

    @property
    def priority_display(self):
        return self.Priority.display(self.priority)

    def _test_expiration(self):
        """ This method tests whether the due_date is in the past and then
            marks the status as 'expired'.
        """
        now = timezone.now()
        if self.due_date < now and self.status == self.Status.todo:
            self.status = self.Status.expired
            self.save()

    @property
    def status_display(self):
        self._test_expiration()
        return self.Status.display(self.status)

    @property
    def is_done(self):
        return self.status == self.Status.done

    @property
    def is_expired(self):
        self._test_expiration()
        return self.status == self.Status.expired

    @property
    def is_todo(self):
        return self.status == self.Status.todo

    @property
    def is_low(self):
        return self.priority == self.Priority.low

    @property
    def is_medium(self):
        return self.priority == self.Priority.medium

    @property
    def is_high(self):
        return self.priority == self.Priority.high

    def as_dict(self):
        """ Useful for AJAX vies and the RESTful API.
        """
        return dict(
            description=self.description,
            due_date=str(self.due_date).split('+')[0],
            priority=self.priority,
            status=self.status,
            user=self.user.id
        )
