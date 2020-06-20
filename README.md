When in this folder with the Dockerfile, do:

docker build -t flaskrunner:latest .

to create an image.  This has python and flask.

When ready to start the server, do

docker run -it -v `pwd`:/web -p 5000:5000 flaskrunner

You'll get a new prompt once in the container.

To start, simply run:

python3 setup.py


