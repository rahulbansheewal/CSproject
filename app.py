from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import jwt
import datetime

SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Server is running")
        elif self.path == "/api/token":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            token = self.generate_token()
            self.wfile.write(json.dumps({'token': token}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/purchase":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                token = self.headers.get('Authorization')
                if not token or not self.verify_token(token):
                    self.send_response(401)
                    self.end_headers()
                    return

                if not self.validate_schema(data):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid data schema")
                    return

                self.insert_data(data)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"POST request received")
            except Exception as e:
                print(f"Error handling POST request: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def generate_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return True
        except jwt.InvalidTokenError:
            return False

    def validate_schema(self, data):
        required_fields = ['name', 'date', 'time', 'item', 'quantity', 'payment', 'role', 'location']
        for field in required_fields:
            if field not in data:
                return False
        return True

    def insert_data(self, data):
        try:
            conn = sqlite3.connect('canteen.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO canteen_purchases (name, date, time, item, quantity, payment, role, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['name'], data['date'], data['time'], data['item'], data['quantity'], data['payment'], data['role'], data['location']))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inserting data into database: {e}")
            raise

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
