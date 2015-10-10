from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import logging
import sofa
from wsgicors import CORS

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    sofa.configure(sqla_session=DBSession, api_config_path=settings['api_config_location'])
    config = Configurator(root_factory=sofa.TraversalRoot, settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include('sofa')
    config.scan()
    return CORS(config.make_wsgi_app(), headers="*", methods="*", maxage="1728000", credentials="true", origin="*")
