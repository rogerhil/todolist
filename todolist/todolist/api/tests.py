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


from tastypie.test import ResourceTestCase

from django.contrib.auth.models import User

from todolist.api.authentication import *
from todolist.todo.models import Todo


class TodoResourceTest(ResourceTestCase):

    fixtures = ['test_todo.json']

    def setUp(self):
        super(TodoResourceTest, self).setUp()

        # Create a user.
        self.username = 'rogerhil'
        self.password = 'password'
        self.email = 'rogerhil@gmail.com'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.user.is_superuser = True
        self.user.save()

        td = Todo.objects.get(pk=1)
        self.todo_1 = Todo.objects.create(description=td.description,
                                    due_date=td.due_date, priority=td.priority,
                                    user=self.user)

        self.detail_url = '/api/todo/{0}/'.format(self.todo_1.pk)

        self.post_data = {
            u'description': u'Todo description posted 1',
            u'priority': 3,
            u'due_date': '2014-02-25 15:00'
        }

    def get_credentials(self):
        return self.create_apikey(self.username, self.user.api_key.key)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/todo/',
                                                        format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/todo/', format='json',
                                   authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 1)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url,
                                                        format='json'))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json',
                                   authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
        self.assertKeys(self.deserialize(resp), ['description', 'priority',
                                                 'status', 'due_date',
                                                 'id', 'resource_uri'])

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/todo/',
                                        format='json', data=self.post_data))

    def test_post_list(self):
        self.assertEqual(Todo.objects.filter(user=self.user).count(), 1)
        self.assertHttpCreated(self.api_client.post('/api/todo/',
                                                    format='json',
                  data=self.post_data, authentication=self.get_credentials()))
        self.assertEqual(Todo.objects.filter(user=self.user).count(), 2)

        resp = self.api_client.get('/api/todo/', format='json',
                                   authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 2)

        self.assertEqual(self.deserialize(resp)['objects'][1], {
            u'description': self.post_data['description'],
            u'priority': self.post_data['priority'],
            u'due_date': unicode(self.post_data['due_date'].replace(' ', 'T') + ':00'),
            u'resource_uri': u'/api/todo/5/',
            u'status': u'todo',
            u'id': 5
        })

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url,
                                                       format='json', data={}))

    def test_put_detail(self):
        original_data = self.deserialize(self.api_client.get(self.detail_url,
                         format='json', authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['description'] = 'Updated: todo 1'
        new_data['due_date'] = '2014-05-13 20:00'
        self.assertEqual(Todo.objects.count(), 4)
        self.assertHttpAccepted(self.api_client.put(self.detail_url,
          format='json', data=new_data, authentication=self.get_credentials()))
        self.assertEqual(Todo.objects.count(), 4)
        self.assertEqual(Todo.objects.get(pk=4).description,
                         new_data['description'])
        self.assertEqual(Todo.objects.get(pk=4).priority, 3)

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url,
                                                           format='json'))

    def test_delete_detail(self):
        self.assertEqual(Todo.objects.count(), 4)
        self.assertHttpAccepted(self.api_client.delete(self.detail_url,
                         format='json', authentication=self.get_credentials()))
        self.assertEqual(Todo.objects.count(), 3)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
