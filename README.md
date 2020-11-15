

# Instalación Nginx, Gunicorn y Supervisor
## referencias: 
- https://www.hektorprofe.net/tutorial/django-ubuntu-server-nginx-gunicorn-supervisor
- pipenv + gunicorn https://www.fatalerrors.org/a/deployment-of-flask-web-site-with-pipenv-gunicorn-supervisor-under-centos.html


## Supervisor
ComprasPublicas.conf
"""
[program:liciorion.com]
command =  /home/ubuntu/.local/bin/pipenv run /home/ubuntu/.local/share/virtualenvs/ComprasPublicas-8kMO_B0Y/bin/gunicorn compras_publicas.wsgi:application --bind=172.31.91.199:8000
directory = /home/ubuntu/ComprasPublicas
user = ubuntu
"""

## NGINX
ComprasPublicas.com
"""
server {

    # Puerto y nombre
    listen 80;
    server_name ec2-3-92-212-32.compute-1.amazonaws.com;

    # Logs de nginx
    access_log /home/ubuntu/logs/nginx.access.log;
    error_log  /home/ubuntu/logs/nginx.error.log;

    # Ficheros estáticos
    location /static/ {
        alias /home/ubuntu/ComprasPublicas/staticfiles/;
        expires 365d;
    }

    # Proxy reverso del puerto 8000
    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 1m;
        proxy_connect_timeout 1m;
        proxy_pass http://172.31.91.199:8000;
    }

}
"""