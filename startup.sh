sudo screen -S rgb uwsgi --socket 0.0.0.0:5000 --protocol=http --master --enable-threads -w wsgi:app
