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
        self.post_data1 = dict(
            username='',
            email='anotheruser@example.com',
            password1='anotherpassword',
            password2='anotherpassword'
        )
        self.post_data2 = dict(
            username='anotheruser',
            email='anotheruser@example.com',
            password1='anotherpassword',
            password2='anotherpasswor'
        )
        self.post_data3 = dict(
            username='anotheruser',
            email='anotheruser@example.com',
            password1='anotherpassword',
            password2='anotherpassword'
        )

    def test_sign_in(self):
        self.assertEquals(User.objects.all().count(), 1)
        url = reverse('todo_listing')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        url2 = self.path(reverse('sign_in')[:-1], 'next=%s' % url)
        self.assertEquals(response['location'], url2)
        url = reverse('sign_in')
        response = self.client.post(url, dict(username=self.username))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.content.find('This field is required') != -1)
        response = self.client.post(url, dict(username=self.username,
                                              password=self.password))
        self.assertEquals(response.status_code, 302)
        url2 = self.path(reverse('home')[:-1], '')
        self.assertEquals(response['location'], url2.replace('?', '/'))
        url = reverse('todo_listing')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_sign_up(self):
        self.assertEquals(User.objects.all().count(), 1)
        url = reverse('sign_up')
        response = self.client.post(url, self.post_data1)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.content.find('This field is required') != -1)
        response = self.client.post(url, self.post_data2)
        self.assertEquals(response.status_code, 200)
        msg = "The two password fields didn&#39;t match."
        self.assertTrue(response.content.find(msg) != -1)
        response = self.client.post(url, self.post_data3)
        self.assertEquals(response.status_code, 302)
        url2 = self.path(reverse('home')[:-1], '')
        self.assertEquals(response['location'], url2.replace('?', '/'))

    def test_sign_out(self):
        self.test_sign_in()
        url = reverse('sign_out')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 301)
        url2 = self.path(reverse('home')[:-1], '')
        self.assertEquals(response['location'], url2.replace('?', '/'))
        url = reverse('todo_listing')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        url2 = self.path(reverse('sign_in')[:-1], 'next=%s' % url)
        self.assertEquals(response['location'], url2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
