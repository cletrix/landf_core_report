from views.base_handler import BaseHandler
import json
import constants


class FrontPage(BaseHandler):
    def get(self):
        try:
            response = {
                'version': str(constants.VERSION),
                'command': 'frontpage',
                'title': 'Report',
                'req_per_seconds': BaseHandler.speed,
                'port': f'{constants.PORT}',
                'start_time': f'{constants.START_TIME}',
            }

            self.write(response)
        except json.JSONDecodeError:
            self.set_status(400)  # Bad Request
            self.write({'command': 'play', "status": "error", "message": "JSON invalid"})
        except Exception as e:
            self.set_status(500)  # Internal Server Error
            self.write({'command': 'play', "status": "error", "message": "Internal Error", "details": str(e)})
