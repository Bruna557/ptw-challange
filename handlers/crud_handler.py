import functools
import httplib
from logzero import logger
import json

from .base_handler import BaseHandler
from exception.enitity_not_found import EntityNotFound


class CrudHandler(BaseHandler):

    repository = NotImplementedError

    # pylint: disable=no-method-argument
    def handle():
        def decorator(function):
            @functools.wraps(function)
            def wrapper(self, *args):
                try:
                    result = function(self, *args)
                    self.write_response(status_code=httplib.OK,result=result)
                except EntityNotFound:
                    logger.error("Entity not found")
                    self.write_error(status_code=httplib.NOT_FOUND,
                                        message="entity not found")
                except Exception as err:
                    logger.error(str(err))
                    self.write_error(status_code=httplib.INTERNAL_SERVER_ERROR,
                                        message=str(err))
            return wrapper
        return decorator

    @handle()
    def get(self, key):
        if not key:
            return self.repository.get_all()
        else:
            return self.repository.get_by_id(key)

    @handle()
    def post(self, key):
        return self.repository.save(json.loads(self.request.body))

