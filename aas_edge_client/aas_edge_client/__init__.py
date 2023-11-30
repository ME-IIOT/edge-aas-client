default_app_config = 'aas_edge_client.apps.AasEdgeClientConfig'

from .celery import app as celery_app

__all__ = ('celery_app',)