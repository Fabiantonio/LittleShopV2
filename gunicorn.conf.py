# Configuración de Gunicorn para Render

bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1200
max_requests_jitter = 50
reload = False

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"