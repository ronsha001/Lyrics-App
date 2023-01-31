import requests
import time

def song_test(song_name):
  start = time.time()
  try:
    r = requests.get(f"http://localhost/lyrics?song={song_name}")
  except:
    raise Exception("Something went wrong.")
  end = time.time()
  print(r.text+"\n")
  return end - start

def tests(songs):
  for song in songs:
    print(f"Test song: {song} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    test_no_cache = song_test(song)
    test_with_cache = song_test(song)
    if (test_with_cache > 0.05):
      raise Exception(f"Failed performance test, song request took {test_with_cache}s. The minimum requirment to pass performance test is 0.05s and lower.")

songs_list = ["Halla Madrid", "Toxicity", "Nothing Else Matter", "No woman no cry", "Diary of Jane"]

tests(songs_list)

print("Tests passed successfully :)")

