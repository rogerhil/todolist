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

""" Contains the base forms classes for TodoList.
"""

from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.html import format_html, format_html_join

from todolist.noconflict import classmaker


@python_2_unicode_compatible
class BootstrapErrorList(ErrorList):
    """ A collection of errors that knows how to display itself in Bootstrap
        format.
    """
    def __str__(self):
        """ Retrieves as default the as_bootstrap() formatted.
        """
        return self.as_bootstrap()

    def as_bootstrap(self):
        """ Retrieves a html formatted for the bootstrap.
        """
        if not self:
            return ''
        t = '<label class="control-label">{0}</label>'
        text = format_html_join('', t, ((force_text(e),) for e in self))
        return format_html('{0}', text)


class BootstrapDatetimeBoundField(forms.forms.BoundField):
    """ This is the overwritten BoundField class to make the form compatible
        with bootstrap datetimepicker.
    """
    add_on = '<span class="add-on"><i data-time-icon="icon-time" '\
             'data-date-icon="icon-calendar"></i></span>'

    def as_widget(self, *args, **kwargs):
        """ Includes the 'datetimepicker' class in the field.
        """
        if not kwargs.has_key('attrs'):
            kwargs['attrs'] = {}
        kwargs['attrs']['data-format'] = "dd/MM/yyyy hh:mm:ss"
        t = super(BootstrapDatetimeBoundField, self).as_widget(*args, **kwargs)
        t = t.replace('class="', 'class="datetimepicker ')
        t += self.add_on
        return t


class BootstrapForm(forms.Form):
    """ This class overrides some necessary methods for compatibility with
        the css classes of bootstrap.
    """

    input_class = 'form-control'
    error_css_class = 'has-error'
    required_css_class = 'form-group input-append date'

    def __init__(self, *args, **kwargs):
        """ Overrides the constructor forcing our new BootstrapErrorList error
            class.
        """
        super(BootstrapForm, self).__init__(*args, **kwargs)
        self.error_class = BootstrapErrorList

    def __getitem__(self, *args, **kwargs):
        """ Forces the css class of each field widget to be the
            self.input_class. Also adds a new attr placeholder to be the
            field label.
        """
        bf = super(BootstrapForm, self).__getitem__(*args, **kwargs)
        bf.field.widget.attrs['class'] = self.input_class
        bf.field.widget.attrs['placeholder'] = bf.field.label
        if isinstance(bf.field, forms.DateTimeField):
            bf = BootstrapDatetimeBoundField(self, bf.field, bf.name)
        return bf

    def as_bootstrap(self):
        """ Returns this form rendered as HTML bootstrap form format.
        """
        normal_row = '<div %(html_class_attr)s>%(errors)s '\
                     '%(field)s%(help_text)s</div>'
        error_row = '<div class="alert alert-danger">%s</div>'
        row_ender = '</div>'
        help_text_html = ' <span class="helptext">%s</span>'
        return self._html_output(normal_row, error_row, row_ender,
                                 help_text_html, False)

    def as_bootstrap_sided(self):
        """ Returns this form rendered as HTML bootstrap form with
            fields side by side.
        """
        self.required_css_class += ' form-sided'
        normal_row = '<div %(html_class_attr)s> '\
                     '%(field)s%(help_text)s %(errors)s</div>'
        error_row = '<div class="alert alert-danger">%s</div>'
        row_ender = '</div>'
        help_text_html = ' <span class="helptext">%s</span>'
        return self._html_output(normal_row, error_row, row_ender,
                                 help_text_html, False)

    @classmethod
    def transform(cls, form_class):
        """ Transforms a FormClass into a BootstrapForm compatible.
        """
        class NewClass(BootstrapForm, form_class):
            __metaclass__ = classmaker()
        return NewClass
