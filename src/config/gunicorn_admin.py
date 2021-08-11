command = '/home/admin/Project/heisemployers/venv/bin/gunicorn'
pythonpath = '/home/admin/Project/heisemployers/src'
bind = '127.0.0.1:8003'
workers = 5 # CPU * 2 + 1
user = 'admin'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings.admin.prod'
