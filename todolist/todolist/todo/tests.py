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

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import simplejson

from todolist.todo.models import Todo

class TodoTestCase(TestCase):

    def setUp(self):
        self.username = 'someuser'
        self.password = 'password'
        self.email = 'someuser@example.com'
        self.user = User.objects.create_user(username=self.username,
                                             email=self.email,
                                             password=self.password)
        self.client = Client()
        self.base_url = 'http://testserver'
        self.path = lambda x, q: "%s%s?%s" % (self.base_url, x, q)
        self.post_data = dict(
            description='Description 1',
            priority=Todo.Priority.high,
            due_date='2014-03-01 10:30'
        )

    def login(self):
        login_data = {
            'username': self.username,
            'password': self.password
        }
        self.client.login(**login_data)

    @override_settings(CSRF_DISABLED=True)
    def test_listing(self):
        self.assertEquals(Todo.objects.all().count(), 0)
        url = reverse('todo_listing')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        url2 = self.path(reverse('sign_in')[:-1], 'next=%s' % url)
        self.assertEquals(response['location'], url2)
        self.login()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add(self):
        self.login()
        self.assertEquals(Todo.objects.all().count(), 0)
        url = reverse('todo_add')
        response = self.client.post(url, data=self.post_data)
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))

    def test_delete(self):
        self.test_add()
        url = reverse('todo_delete', args=(1,))
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))

    def test_change_description(self):
        self.test_add()
        url = reverse('todo_change_description', args=(1,))
        desc = 'TEST'
        response = self.client.post(url, data=dict(description=desc))
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))
        self.assertGreater(Todo.objects.all().count(), 0)
        td = Todo.objects.get(pk=1)
        self.assertEquals(td.description, desc)

    def test_change_duo_date(self):
        self.test_add()
        url = reverse('todo_change_due_date', args=(1,))
        dd = '2014-04-01 23:59'
        response = self.client.post(url, data=dict(due_date=dd))
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))
        self.assertGreater(Todo.objects.all().count(), 0)
        td = Todo.objects.get(pk=1)
        self.assertEquals(td.due_date.strftime('%Y-%m-%d %H:%M'), dd)

    def test_mark_as_done(self):
        self.test_add()
        url = reverse('todo_mark_done', args=(1,))
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))
        self.assertGreater(Todo.objects.all().count(), 0)
        td = Todo.objects.get(pk=1)
        self.assertEquals(td.status, Todo.Status.done)

    def test_change_priority(self):
        self.test_add()
        url = reverse('todo_change_priority', args=(1,))
        response = self.client.post(url, dict(priority=Todo.Priority.medium))
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))
        self.assertGreater(Todo.objects.all().count(), 0)
        td = Todo.objects.get(pk=1)
        self.assertEquals(td.priority, Todo.Priority.medium)

    def test_reload(self):
        self.test_add()
        url = reverse('todo_listing_relaod')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        rdata = simplejson.loads(response.content)
        self.assertTrue(rdata.get('success'))
        self.assertIsNotNone(rdata.get('content'))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
