#!/usr/bin/env bash
# Configures a new Ubuntu machine with nginx - 
apt-get -y update && apt-get -y install nginx 
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html 
ln -sf  /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
rm -f /etc/nginx/sites-enabled/default 
echo -e "
server {
	listen 80 default_server;
	root /data/;
	index index.html index.htm;
	add_header X-Served-By \$hostname;	

	location / {
		root /srv/www;
		index index.html;
	}

	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
	}

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html;
	}
}" | sudo tee /etc/nginx/sites-available/www 
ln -sf /etc/nginx/sites-available/www /etc/nginx/sites-enabled/ 
sudo nginx -t && sudo service nginx restart
