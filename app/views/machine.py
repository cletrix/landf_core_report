from views.base_handler import BaseHandler
import json
from datetime import datetime
from core.manager import Manager


class Machine(BaseHandler):

    async def post(self):
        data = json.loads(self.request.body)
        place = data.get('place')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not place or not start_date or not end_date:
            self.set_status(400)
            self.write({"error": "Missing required parameters: place, start_date, end_date"})
            return

        response = await Manager.machine(place, start_date, end_date)

        json_response = []
        for row in response:
            json_response.append({
                'Datetime': row[0].isoformat() if isinstance(row[0], datetime) else row[0],
                'Value': row[1],
                'Type': row[2],
                'Login': row[3],
                'Location': row[4],
                'ID': row[5]
            })

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(json_response))
        self.finish()

# curl -X POST http://jane.cletrix.net:33444/machine \
#      -H "Content-Type: application/json" \
#      -d '{
#            "place": "local1",
#            "start_date": "2024-01-01",
#            "end_date": "2024-12-31"
#          }'
