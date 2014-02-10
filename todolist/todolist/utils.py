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

""" Contains utils classes and functions.
"""


class Choices:
    """ Base class for choices classes.
    
    >>> class ChordType(Choices):
    ...     major = 1
    ...     minor = 2

    >>> ChordType.choices()
    [(1, 'Major'), (2, 'Minor')]
    """

    @classmethod
    def choices(cls):
        """ Provides a list of tuples containing (value, class attribute name).
            It reads the current class attributes through the "dir" function
            ignoring those starting with '__'.
        """
        choices = [(getattr(cls, i), i.title()) for i in dir(cls)
                                                if not i.startswith('__') and
                                      not hasattr(getattr(cls, i), '__call__')]
        choices.sort()
        return choices

    @classmethod
    def display(cls, key):
        """ Returns the title value of a choice.
        """
        return dict(cls.choices()).get(key)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
