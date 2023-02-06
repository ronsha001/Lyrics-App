from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import requests
import redis
import os

app = Flask(__name__)
CORS(app)

REDIS_DNS = os.environ.get("REDIT_DNS")
REDIS_PORT = os.environ.get("REDIS_PORT")

try:
  REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
  r = redis.Redis(host=REDIS_DNS, port=REDIS_PORT, password=REDIS_PASSWORD)
  print("Connected (with password) to redis.")
except:
  print("No password is needed for redis.")
  r = redis.Redis(host=REDIS_DNS, port=REDIS_PORT)
  print("Connected to redis.")

DEFAULT_EXECUTE_TIME = os.environ.get("DEFAULT_EXECUTE_TIME")
PORT = os.environ.get("PORT")


@app.route("/")
def general_room():
  return render_template('index.html')

@app.route("/health")
def health():
  return "OK"

@app.route("/lyrics")
def lyrics():
  song_name = request.args.get('song')
  lyrics = get_lyrics(song_name)
  return lyrics


def get_lyrics(song):
  try:
    cache = r.get(song)
    if cache:
      print("CACHE HIT")
      return cache
    else:
      print("CACHE MISS")
      data = requests.get(f"https://www.google.com/search?q={song} lyrics")
      html = data.text
      start_delimiter = '</span></div></div></div></div><div class="hwc"><div class="BNeawe tAd8D AP7Wnd"><div><div class="BNeawe tAd8D AP7Wnd"><span dir="ltr">'
      end_delimiter = "</span></div></div></div></div></div>"
      start_index = html.find(start_delimiter) + len(start_delimiter)
      end_index = html.find(end_delimiter)
      r.setex(song, DEFAULT_EXECUTE_TIME, html[start_index:end_index])

    return html[start_index:end_index]
  except Exception as err:
    print(f"Something went wrong! {err}")



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=PORT)
