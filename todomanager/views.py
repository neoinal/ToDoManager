from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return Response("This page does not created yet.", content_type='text/plain', status_int=500)
