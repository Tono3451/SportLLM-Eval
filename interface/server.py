import http.server
import socketserver
import json
from pathlib import Path
import sys

PORT = 8000
# El script está en interface/, así que subimos un nivel para tener el workspace root
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = WORKSPACE_ROOT / "results"

class DynamicResultHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Servimos los archivos desde el nivel raíz (. / tft-pruebas) 
        # para que resuelvan bien /interface/... y /results/...
        super().__init__(*args, directory=str(WORKSPACE_ROOT), **kwargs)

    def do_GET(self):
        # Esta es nuestra "API" para leer las carpetas de resultados dinámicamente
        if self.path == '/api/results':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            
            items = []
            if RESULTS_DIR.exists():
                for file_path in sorted(RESULTS_DIR.rglob("*.jsonl")):
                    # Obtenemos la ruta relativa para los grupos (subcarpetas)
                    rel_path = file_path.relative_to(RESULTS_DIR).as_posix()
                    items.append({
                        "file_name": rel_path,
                        "label": rel_path.replace(".jsonl", "")
                    })
            
            self.wfile.write(json.dumps(items, ensure_ascii=False).encode('utf-8'))
            return
        
        # Al acceder a "localhost:8000" o al "/" redireccionamos al index.html
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/interface/index.html')
            self.end_headers()
            return

        # Para el resto de archivos (html, js, css, jsonl...), usamos el servidor estático normal
        return super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DynamicResultHandler) as httpd:
        print(f"Servidor iniciado. Abre tu navegador en: http://localhost:{PORT}")
        print("Presiona Ctrl+C para detener el servidor.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
            sys.exit(0)