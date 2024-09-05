# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html
# https://adamj.eu/tech/2021/12/29/set-up-a-gunicorn-configuration-file-and-test-it/
import multiprocessing
from pathlib import Path

max_requests = 1000
max_requests_jitter = 50

reload = True
reload_engine = "inotify"
reload_extra_files = ["/code/apps/", "/code/templates/"]

log_file = "-"

bind = "0.0.0.0:9637"
workers = 2
