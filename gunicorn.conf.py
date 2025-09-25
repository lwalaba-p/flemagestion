# Configuration Gunicorn pour Render
import multiprocessing

# Nombre de workers
workers = multiprocessing.cpu_count() * 2 + 1

# Configuration des workers
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Configuration du serveur
bind = '0.0.0.0:8000'
backlog = 2048

# Configuration des logs
loglevel = 'info'
accesslog = '-'
errorlog = '-'

# Configuration de sécurité
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuration de performance
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Configuration des timeouts
graceful_timeout = 30
worker_tmp_dir = '/dev/shm'
