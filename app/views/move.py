from views.base_handler import BaseHandler
import json
import csv
import io
from core.manager import Manager


class Move(BaseHandler):

    async def get(self):
        place = self.get_argument('place', None)
        start_date = self.get_argument('start_date', None)
        end_date = self.get_argument('end_date', None)
        login = self.get_argument('login', None)

        if not place or not start_date or not end_date or not login:
            self.set_status(400)
            self.write("Missing required parameters: place, start_date, end_date, login")
            return

        response = await Manager.move(place, start_date, end_date, login)

        headers = ['Timestamp', 'ID Match', 'ID Game', 'Credit', 'Value', 'Kind', 'Login', 'Counter In', 'Counter Out']
        rows = [headers] + [list(map(str, row)) for row in response]

        col_widths = [max(len(str(item)) for item in col) for col in zip(*rows)]
        separator = '+'.join('-' * (width + 2) for width in col_widths)

        def format_row(row):
            return '| ' + ' | '.join(f'{item:{width}}' for item, width in zip(row, col_widths)) + ' |'

        table = [separator, format_row(headers), separator]
        for row in rows[1:]:
            table.append(format_row(row))
        table.append(separator)

        self.set_header('Content-Type', 'text/plain')
        self.write('\n'.join(table))

    async def post(self):
        data = json.loads(self.request.body)
        place = data.get('place')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        login = data.get('login')

        if not place or not start_date or not end_date or not login:
            self.set_status(400)
            self.write("Missing required parameters: place, start_date, end_date, login")
            return

        response = await Manager.move(place, start_date, end_date, login)

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['Timestamp', 'ID Match', 'ID Game', 'Credit', 'Value', 'Kind', 'Login', 'Counter In', 'Counter Out'])
        for row in response:
            writer.writerow(row)

        csv_data = output.getvalue()
        output.close()

        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition', 'attachment; filename=move_report.csv')
        self.write(csv_data)
        self.finish()
