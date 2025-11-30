"""
Simple HTTP Server for Frontend
"""

import http.server
import socketserver
import os
import sys

# Change to frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), 'social-media-frontend')
os.chdir(frontend_dir)

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

Handler = CustomHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"{'='*60}")
    print(f"🚀 Frontend Server Started")
    print(f"{'='*60}")
    print(f"")
    print(f"📱 Frontend URL: http://localhost:{PORT}")
    print(f"🔗 Backend URL: http://localhost:8000/graphql/")
    print(f"")
    print(f"{'='*60}")
    print(f"")
    print(f"Press Ctrl+C to stop the server")
    print(f"")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        sys.exit(0)
