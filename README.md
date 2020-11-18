

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
    server_name ec2-3-92-212-32.compute-1.amazonaws.com liciorion.com www.liciorion.com;

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

# Agregar Google Analytics a Django

- https://bhoey.com/blog/adding-google-analytics-to-django-templates/

# How to host GoDaddy domain with AWS EC2
http://sandny.com/2019/11/23/host-godaddy-domain-with-aws-ec2/

# Validar DNS de un dominio
https://www.ultratools.com/tools/dnsLookupResult

# Crear y descargar certificados SSL
https://app.zerossl.com

# Configurar SSL https en NGINX AWS EC2
https://medium.com/datadriveninvestor/nginx-server-ssl-setup-on-aws-ec2-linux-b6bb454e2ef2