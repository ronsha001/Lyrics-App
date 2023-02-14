from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import requests
import redis
import os

app = Flask(__name__)
CORS(app)

REDIS_DNS = os.environ.get("REDIS_DNS")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

if REDIS_PASSWORD:
  r = redis.Redis(host=REDIS_DNS, port=REDIS_PORT, password=REDIS_PASSWORD)
  print("Connected (with password) to redis.")
else:
  print("No password is needed for redis.")
  r = redis.Redis(host=REDIS_DNS, port=REDIS_PORT)
  print("Connected to redis.")

DEFAULT_EXECUTE_TIME = os.environ.get("DEFAULT_EXECUTE_TIME")
PORT = os.environ.get("PORT")


@app.route("/")
def general_room():
  """ Main window/home page of the app

  Returns:
      _type_: file (html)
  """
  return render_template('index.html')

@app.route("/health")
def health():
  """ Simple health check.

  Returns:
      _type_: text_
  """
  return "OK"

@app.route("/lyrics")
def lyrics():
  """ API Route to get lyrics of a sing, it is expecting song argument.

  Returns:
      _type_: text
  """
  song_name = request.args.get('song')
  song_lang = request.args.get('lang')
  lyrics = get_lyrics(song_name, song_lang)
  print(lyrics)
  return lyrics


def get_lyrics(song, song_lang):
  """ This function search for lyrics in Google, by making an http request to google and manipulating the data.

  Args:
      song (string): song name to search

  Returns:
      _type_: string (string of lyrics)
  """

  try:
    if song_lang == None or song == None or song_lang != "en" or song_lang != "he":
      raise Exception("Error: no language or song name specified")
    cache = r.get(song)
    if cache:
      print("CACHE HIT")
      return cache
    else:
      print("CACHE MISS")
      data = requests.get(f"https://www.google.com/search?q={song} lyrics")
      html = data.text

      if song_lang == "en":
        start_delimiter = '</span></div></div></div></div><div class="hwc"><div class="BNeawe tAd8D AP7Wnd"><div><div class="BNeawe tAd8D AP7Wnd"><span dir="ltr">'
        end_delimiter = "</span></div></div></div></div></div>"
      elif song_lang == "he":
        start_delimiter = '</div></div></div></div><div class="hwc"><div class="BNeawe tAd8D AP7Wnd"><div><div class="BNeawe tAd8D AP7Wnd">'
        end_delimiter = '</div></div></div></div></div><div><span class="hwc"><div class="BNeawe uEec3 AP7Wnd">'

      start_index = html.find(start_delimiter) + len(start_delimiter)
      end_index = html.find(end_delimiter)
      r.setex(song, DEFAULT_EXECUTE_TIME, html[start_index:end_index])

    return html[start_index:end_index], 200
  except Exception as err:
    print(f"Something went wrong! {err}")
    return f"Something went wrong! {err}", 400



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=PORT)
