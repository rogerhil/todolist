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

""" The TodoList Auth module.
    Contains the followin views:
     - SignIn
     - SignOut
     - SignUp
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.views.generic import FormView, RedirectView, CreateView

from todolist.forms import BootstrapForm
from todolist.tdauth.decorators import login_required


class SignIn(FormView):
    """ The sign in view
    """
    form_class = BootstrapForm.transform(AuthenticationForm)
    template_name = "tdauth/login.html"

    def form_valid(self, form):
        """ Triggers the login Django action after authentication made by
            the AuthenticationForm form.
        """
        response = super(SignIn, self).form_valid(form)
        login(self.request, form.user_cache)
        return response

    def get_success_url(self):
        """ Retrieves the success url, in this case the home page or an url
            comming from next query string argument. Also leaves a success
            message to the user.
        """
        url = self.request.GET.get('next', reverse('home'))
        messages.success(self.request, "You are now signed in.")
        return url

    def get_context_data(self, **kwargs):
        """ Returns the context data with a next argument.
        """
        kwargs = super(SignIn, self).get_context_data(**kwargs)
        kwargs.update({'next': self.request.GET.get('next')})
        return kwargs


class SignOut(RedirectView):
    """ The sign out view
    """
    pattern_name = 'home'

    def dispatch(self, request, *args, **kwargs):
        """ Triggers the logout Django action.
        """
        logout(request)
        return super(SignOut, self).dispatch(request, *args, **kwargs)


class SignUp(CreateView):
    """ The sign up view
    """
    form_class = BootstrapForm.transform(UserCreationForm)
    template_name = 'tdauth/signup.html'

    def form_valid(self, form):
        """ If the form is valid, save the associated model.
        """
        response = super(SignUp, self).form_valid(form)
        data = form.cleaned_data
        user = self.object
        user = authenticate(username=user.username, password=data['password1'])
        login(self.request, user)
        return response

    def get_success_url(self):
        """ Retrieves the success url, in this case the home page. Also leaves
            a success message to the user.
        """
        messages.success(self.request, "You are now signed in.")
        return reverse('home')
