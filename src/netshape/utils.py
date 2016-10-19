"""Utility classes and functions"""

def serve(ns, _, arg, *args, **kwargs):
    """Utility"""
    try:
        import http.server
        shs = http.server.SimpleHTTPRequestHandler
        import socketserver as ss
    except ImportError:
        from SimpleHTTPServer import SimpleHTTPRequestHandler as shs
        import SocketServer as ss
    port = arg["p"]
    handler = shs
    httpd = ss.TCPServer(("", port), handler)
    print("serving at port", port)
    print("type ^C to exit")
    httpd.serve_forever()