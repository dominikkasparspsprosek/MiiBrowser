"""
Simple test server for testing relative links in MiiBrowser

This creates a local HTTP server with test pages that have relative links.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves test pages"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        # Serve different pages based on path
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Home - Relative Links Test</title>
</head>
<body>
    <h1>Home Page</h1>
    <p>This is the home page.</p>
    <ul>
        <li><a href="/about">About Page (absolute path)</a></li>
        <li><a href="/contact">Contact Page (absolute path)</a></li>
        <li><a href="subpage.html">Subpage (relative)</a></li>
        <li><a href="/docs/help">Help Docs</a></li>
    </ul>
</body>
</html>
"""
            self.wfile.write(html_content.encode())
            
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>About - Relative Links Test</title>
</head>
<body>
    <h1>About Page</h1>
    <p>You successfully navigated to /about using a relative link!</p>
    <ul>
        <li><a href="/">Back to Home</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
</body>
</html>
"""
            self.wfile.write(html_content.encode())
            
        elif self.path == '/contact':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact - Relative Links Test</title>
</head>
<body>
    <h1>Contact Page</h1>
    <p>You successfully navigated to /contact using a relative link!</p>
    <ul>
        <li><a href="/">Back to Home</a></li>
        <li><a href="/about">About</a></li>
    </ul>
</body>
</html>
"""
            self.wfile.write(html_content.encode())
            
        elif self.path == '/docs/help':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Help - Relative Links Test</title>
</head>
<body>
    <h1>Help Documentation</h1>
    <p>You successfully navigated to /docs/help!</p>
    <ul>
        <li><a href="/">Back to Home</a></li>
        <li><a href="../about">About (parent directory)</a></li>
    </ul>
</body>
</html>
"""
            self.wfile.write(html_content.encode())
            
        else:
            # Default 404
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page <code>{self.path}</code> was not found.</p>
    <p><a href="/">Go to Home</a></p>
</body>
</html>
"""
            self.wfile.write(html_content.encode())

def main():
    """Start the test server"""
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("MiiBrowser Relative Links Test Server")
        print("=" * 60)
        print(f"\nServer running at: http://localhost:{PORT}/")
        print("\nTest this in MiiBrowser:")
        print(f"  1. Open MiiBrowser")
        print(f"  2. Navigate to: http://localhost:{PORT}/")
        print(f"  3. Click the links to test relative URL resolution")
        print("\nPress Ctrl+C to stop the server\n")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()
