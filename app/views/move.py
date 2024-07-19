from views.base_handler import BaseHandler
import json
from datetime import datetime
from core.manager import Manager


class Move(BaseHandler):

    async def post(self):
        data = json.loads(self.request.body)
        place = data.get('place')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not place or not start_date or not end_date:
            self.set_status(400)
            self.write({"error": "Missing required parameters: place, start_date, end_date"})
            return

        response = await Manager.move(place, start_date, end_date)

        json_response = []
        for row in response:
            json_response.append({
                'Timestamp': row[0].isoformat() if isinstance(row[0], datetime) else row[0],
                'ID Match': row[1],
                'ID Game': row[2],
                'Credit': row[3],
                'Value': row[4],
                'Kind': row[5],
                'Login': row[6],
                'Counter In': row[7],
                'Counter Out': row[8]
            })

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(json_response))
        self.finish()

# curl -X POST http://localhost:33444/move \
#      -H "Content-Type: application/json" \
#      -d '{
#            "place": "local1",
#            "start_date": "2024-01-01",
#            "end_date": "2024-12-31"
#          }'
