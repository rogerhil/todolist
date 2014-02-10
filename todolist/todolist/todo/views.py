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

""" Contains the views for the Todo model.
     - Listing
     - Adding
     - Removing
     - Changing

"""

from annoying.decorators import ajax_request

from django.template import loader
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, View, UpdateView
from django.views.generic.list import ListView

from todolist.tdauth.decorators import login_required
from todolist.todo.models import Todo
from todolist.todo.forms import TodoForm


class Listing(ListView):
    """ Main view of Todo List
    """
    model = Todo
    context_object_name = 'todo_list'
    paginate_by = 10
    sorting_fields = [
        'description',
        'due_date',
        'priority',
        'status'
    ]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """ Overrides to set this view as login_required
        """
        return super(Listing, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """ Filter the queryset by the current logged user and also order_by
            request.GET.get('order').
        """
        qs = super(Listing, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        self.order_by = self.fetch_order_by()
        if self.order_by:
            qs = qs.order_by(self.order_by)
        return qs

    def fetch_order_by(self):
        """ Gets the the order_by value through request.GET and verifies
            whether is in the allowed sorting fields.
        """
        order_by = self.request.GET.get('order', '').strip() or None
        if not order_by:
            return
        n = ["-%s" % i for i in self.sorting_fields] + self.sorting_fields
        intersection = set(n).intersection(set([order_by]))
        return list(intersection)[0] if intersection else None

    def get_context_data(self, **kwargs):
        """ This context data also contains the TodoForm, the priority choices
            class, the order_by argument and the order_class to be used in
            the table header.
        """
        self.kwargs = kwargs
        kwargs = super(Listing, self).get_context_data(**kwargs)
        kwargs['form'] = TodoForm()
        kwargs['priority'] = Todo.Priority
        kwargs['order_by'] = self.order_by
        if self.order_by:
            order_class = 'sorting_asc' if self.order_by.startswith('-') \
                                         else 'sorting_desc'
            kwargs['order_class'] = {}
            kwargs['order_class'][self.order_by.replace('-', '')] = order_class
        return kwargs

    def get_listing_content(self):
        """ This method retrieves the listing rendered content, useful for
            the AJAX views
        """
        template = loader.get_template('todo/listing.html')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context = RequestContext(self.request, context)
        return template.render(context)


class ReloadListing(Listing):
    """ This is a AJAX view for the Listing view table content
    """

    @method_decorator(ajax_request)
    def get(self, request, *args, **kwargs):
        """ The get AJAX method for the Listing table
        """
        content = self.get_listing_content()
        return {'success': True, 'content': content}


class CommonAjaxView(View):
    """ This is a base class for AJAX views.
    """

    form_class = TodoForm
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """ Overrides to set this view as login_required
        """
        return super(CommonAjaxView, self).dispatch(request, *args, **kwargs)

    @method_decorator(ajax_request)
    def post(self, request, *args, **kwargs):
        """ Overrides to set the post method as AJAX
        """
        return super(CommonAjaxView, self).post(request, *args, **kwargs)

    def get_listing_content(self):
        """ Retrieves the listing content to update the tables via AJAX
        """
        view = Listing(request=self.request)
        return view.get_listing_content()

    def form_valid(self, form):
        """ If the form is valid, includes the listing content into the JSON
            AJAX response.
        """
        super(CommonAjaxView, self).form_valid(form)
        content = self.get_listing_content()
        return {'success': True, 'content': content}

    def form_invalid(self, form):
        """ If the form is invalid, includes the errors details into the JSON
            AJAX response.
        """
        return {'success': False, 'errors': str(form.errors)}


class ModifyView(View):
    """ This is a base view for the modify views.
    """

    def get_queryset(self):
        """ Filters the queryset with the current authenticated in user.
        """
        qs = super(ModifyView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class Add(CommonAjaxView, CreateView):
    """ The create view for Todo model.
    """

    def get_form_kwargs(self):
        """ Includes the authenticated user in the new Todo object model.
        """
        kwargs = super(Add, self).get_form_kwargs()
        kwargs['instance'] = Todo(user=self.request.user)
        return kwargs

    def form_invalid(self, form):
        """ Retrieves the errors details of the unsuccessful validation and
            also the content of the form with the correspond validation
            messages.
        """
        template = loader.get_template('todo/add_form.html')
        context = RequestContext(self.request, dict(form=form))
        content = template.render(context)
        return {'success': False, 'errors': str(form.errors),
                'content': content}


class Delete(ModifyView, CommonAjaxView, DeleteView):
    """ The delete view for the Todo model.
    """
    model = Todo

    @method_decorator(ajax_request)
    def delete(self, request, *args, **kwargs):
        """ Overrides to set the post method as AJAX and also retrieves the
            listing content.
        """
        super(Delete, self).delete(request, *args, **kwargs)
        content = self.get_listing_content()
        return {'success': True, 'content': content}


class Change(ModifyView, CommonAjaxView, UpdateView):
    """ The base class for the change views.
    """
    model = Todo



class MarkAsDone(Change):
    """ This is the class for the AJAX action: mark the Todo status as 'done'.
    """

    def get_form_kwargs(self, *args, **kwargs):
        """ It includes the object values into the form data to avoid
            required validation errors. This view has only the 'status'
            field as required.
        """
        kwargs = super(MarkAsDone, self).get_form_kwargs(*args, **kwargs)
        obj_dict = self.object.as_dict()
        kwargs['data'] = obj_dict
        return kwargs

    def form_valid(self, form):
        """ Hard coded method to set the Todo.status as 'done'. Also retrieves
            the listing content.
        """
        self.object.status = Todo.Status.done
        self.object.save()
        content = self.get_listing_content()
        return {'success': True, 'content': content}


class ChangePriority(Change):
    """ The change priority view.
    """

    def get_form_kwargs(self, *args, **kwargs):
        """ It includes the object values into the form data to avoid
            required validation errors. This view has only the 'priority'
            field as required.
        """
        kwargs = super(ChangePriority, self).get_form_kwargs(*args, **kwargs)
        obj_dict = self.object.as_dict()
        obj_dict['priority'] = kwargs['data']['priority']
        kwargs['data'] = obj_dict
        return kwargs

    def form_valid(self, form):
        """ Sets only the Todo.priority with the correspond value comming from
            post. Also retrieves the listing content.
        """
        kwargs = self.get_form_kwargs()
        self.object.priority = kwargs['data']['priority']
        self.object.save()
        content = self.get_listing_content()
        return {'success': True, 'content': content}


class ChangeDueDate(Change):
    """ The change due_date view.
    """

    def get_form_kwargs(self, *args, **kwargs):
        """ It includes the object values into the form data to avoid
            required validation errors. This view has only the 'due_date'
            field as required.
        """
        kwargs = super(ChangeDueDate, self).get_form_kwargs(*args, **kwargs)
        obj_dict = self.object.as_dict()
        obj_dict['due_date'] = kwargs['data']['due_date']
        kwargs['data'] = obj_dict
        return kwargs

    def form_valid(self, form):
        """ Sets only the Todo.due_date with the correspond value comming from
            post. Also retrieves the listing content.
        """
        kwargs = self.get_form_kwargs()
        self.object.due_date = kwargs['data']['due_date']
        self.object.save()
        content = self.get_listing_content()
        return {'success': True, 'content': content}


class ChangeDescription(Change):
    """ The change description view.
    """

    def get_form_kwargs(self, *args, **kwargs):
        """ It includes the object values into the form data to avoid
            required validation errors. This view has only the 'description'
            field as required.
        """
        kwargs = super(ChangeDescription, self).get_form_kwargs(*args, **kwargs)
        obj_dict = self.object.as_dict()
        obj_dict['description'] = kwargs['data']['description']
        kwargs['data'] = obj_dict
        return kwargs

    def form_valid(self, form):
        """ Sets only the Todo.description with the correspond value comming
            from post. Also retrieves the listing content.
        """
        kwargs = self.get_form_kwargs()
        self.object.description = kwargs['data']['description']
        self.object.save()
        content = self.get_listing_content()
        return {'success': True, 'content': content}
