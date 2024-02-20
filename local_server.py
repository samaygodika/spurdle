from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8888  # Replace with your desired port

# Create an HTTP server instance
httpd = HTTPServer(('', PORT), SimpleHTTPRequestHandler)

print(f"Serving on port {PORT}")
httpd.serve_forever()