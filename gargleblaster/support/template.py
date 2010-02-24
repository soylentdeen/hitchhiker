
from collections import defaultdict

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateSyntaxError
from django.template.defaultfilters import escapejs
from django.template.loader import render_to_string

_context = dict( ( name, getattr( settings, name, None ) ) for name in settings.EXPOSED_SETTINGS )
settings_processor = lambda request, _context = _context: _context

def contextual_render( request, *arguments, **parameters ):
    """Renders a template using RequestContext."""

    parameters[ 'context_instance' ] = RequestContext( request )
    return render_to_response( *arguments, **parameters )

def escape_node_parameters( parameters ):
    """Suitably escapes the specified node parameters for javascript."""

    return dict( [ ( key, escapejs( value ) ) for key, value in parameters.iteritems() ] )

def parse_node_parameters( parser, token ):
    """Parses template node arguments into a set of parameters."""

    arguments, parameters = token.split_contents(), {}
    for argument in arguments[ 1: ]:
        if '=' in argument:
            param, value = argument.split( '=', 1 )
            parameters[ str( param.lower() ) ] = parser.compile_filter( value )
        else:
            raise TemplateSyntaxError( 'argument must be in name=value format' )
    else:
        return parameters

def render_email_template( template, **context ):
    """Renders an email template using the specified context."""

    subject, body = render_to_string( template, context ).split( '\n', 1 )
    return subject.strip(), body

def resolve_node_parameters( context, parameters ):
    """Resolves the values of the specified parameters against the context."""

    return dict( [ ( str( key ), value.resolve( context ) ) for key, value in parameters.iteritems() ] )

