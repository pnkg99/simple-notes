from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json, random


    
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("notes.json", 'r') as f :
            notes = json.load(f)
        if self.path == '/':
            self.path = '/index.html'
            
        elif self.path == '/add_note':
            self.add_note(notes)
            return
        
        elif self.path == '/notes':
            self.read_notes(notes)
            return 
        
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
            
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        form_data = parse_qs(post_data)

        writer = form_data['writer'][0]
        title = form_data['title'][0]
        content = form_data['content'][0]     
        current_date = str(datetime.now().date())
        
        with open("notes.json", 'r') as f :
            notes = json.load(f)        
        
        note = {"writer" : writer, "title" : title, "content" : content, "date" : current_date }    
        
        try:
            with open("notes.json", "r") as f:
                notes = json.load(f)
        except:
            notes = []
        # append the new note to the list
        notes.append(note)
        # write the notes back to the json file
        with open("notes.json", "w") as f:
            json.dump(notes, f, indent=4)
            
        self.add_note()
        
    def add_note(self):
        message = "<h2>Note added successfully!</h2>"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))

    def read_notes(self, notes):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('notes.html')
        rendered_template = template.render(notes=notes)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(rendered_template, 'utf-8'))
        
        
httpd = HTTPServer(('', 8000), MyHandler)
httpd.serve_forever()