from flask import Flask, render_template
# from rediscluster import RedisCluster
from redis import Redis, RedisError
import os
import socket

# startup_nodes = [{"host": "redis-master.redis.svc.cluster.local", "port":"6379"

redis = Redis(host="redis-master.redis.svc.cluster.local", port=6379, password=REDIS_PASSWORD, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
  try:
    visits = redis.incr("counter")
  except RedisError:
    visits = "<i>cannot connect to Redis, counter disabled</i>"
    
  html = "<h3>Hello {name}!</h3>" \
            "<b>Hostname:</b> {hostname}<br/>" \
            "<b>Visits:</b> {visits}"
            
  return html.format(
          name=os.getenv("NAME", "world"),
          hostname=socket.gethostname(),
          visits=visits
        )

@app.route("/files")
def dirtree():
  path = os.path.expanduser(u'/mnt/fileshare')
  return render_template('dirtree.html', tree=make_tree(path))

def make_tree(path):
  tree = dict(name=path, children=[])
  try: lst = os.listdir(path)
  except OSError:
    pass
  else:
    for name in lst:
      fn = os.path.join(path, name)
      if os.path.isdir(fn):
        tree['children'].append(make_tree(fn))
      else:
        tree['children'].append(dict(name=fn))
  return tree


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80)
  
