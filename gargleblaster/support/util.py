
from inspect import getargspec, stack
from re import compile as regexp
from struct import unpack
from uuid import uuid4

from django.conf import settings

ValidEmail = regexp(
    r"(?i)(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$'
)

def choices( choices ):
    """Constructs a tuple of choices tuples for the specified choices."""

    return tuple( [ ( str( choice ), str( choice ).capitalize() ) for choice in choices ] )

def identify_remote_ip( request ):
    """Identifies the remote ip of the specified request."""

    return request.META.get( 'REMOTE_ADDR' )

def trace_stack( indent = '' ):
    """Traces the stack at the current source line."""

    lines = []
    for frame, filename, lineno, context, source, pos in reversed( stack()[ 1: ] ):
        lines.append( '%sfile "%s", line %d, in %s' % ( indent, filename, lineno, context ) )
        if source:
            lines.append( '%s    %s' % ( indent, source[ 0 ].strip() ) )
    else:
        return '\n'.join( lines )

def uniqid():
    """Generates a 32-character unique identifier."""

    return str( uuid4() ).replace( '-', '' )

def verify_email( email, pattern = ValidEmail ):
    """Verifies the specified email address."""

    return bool( pattern.search( email ) )

