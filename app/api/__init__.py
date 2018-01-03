from flask import Blueprint

api = Blueprint('api', __name__)
api.config = {}

@api.record
def record_params(setup_state):
  app = setup_state.app
  api.config = dict([(key,value) for (key,value) in app.config.items()])

from . import apis