#!/usr/bin/env bash
# setup web server for deployment of web static

sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html>
   <head>
   </head>
   <body>
   Holberton School
   </body>
   </html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubunutu:ubuntu /data/

config="server {
    listen 80;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root /etc/nginx/html;
    index index.html index.htm;

    location /hbnb_static {
    alias /data/web_static/current;
    index index.html index.htm;
}
    error_page 4040 /404.html;
    location /404 {
    root /etc/nginx/html;
    internal;
}
}"

sudo bash -c "echo '$config' > /etc/nginx/sites-available/default"

sudo service nginx restart
