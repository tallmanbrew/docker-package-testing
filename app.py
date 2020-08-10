from flask import Flask
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
          name=os.getenv("NAME", "world 2"),
          hostname=socket.gethostname(),
          visits=visits
        )
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80)
  
