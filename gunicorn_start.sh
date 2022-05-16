#!/bin/bash

NAME="material_project"              #Name of the application (*)
DJANGODIR=./material_project         			# Django project directory (*)
SOCKFILE=./run/gunicorn.sock        		# we will communicate using this unix socket (*)
USER=sanwahost                                  # the user to run as (*)
#GROUP=webdata                                  # the group to run as (*)
NUM_WORKERS=1                                  # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=material_project.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=material_project.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `material_project`"

# Activate the virtual environment
cd $DJANGODIR
source ./venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ./venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
