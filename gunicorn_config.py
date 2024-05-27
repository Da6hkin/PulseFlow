bind = "0.0.0.0:8000"
module = "PulseFlow.wsgi:application"

workers = 5
worker_connections = 1000
threads = 5

certfile = "/etc/letsencrypt/live/pulseflow.xyz/fullchain.pem"
keyfile = "/etc/letsencrypt/live/pulseflow.xyz/privkey.pem"
