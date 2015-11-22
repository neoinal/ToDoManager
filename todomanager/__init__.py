import hashlib
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    secret = hashlib.sha256(str(settings['pyramid.session.secret']).encode('utf-8')).hexdigest()
    session_factory = SignedCookieSessionFactory(secret=secret)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('create', '/create')
    config.scan()
    return config.make_wsgi_app()
