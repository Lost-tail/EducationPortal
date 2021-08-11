#!/bin/bash
source /home/admin/Project/heisemployers/venv/bin/activate
gunicorn -c "/home/admin/Project/heisemployers/src/config/gunicorn_main.py" config.wsgi
