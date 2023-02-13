import requests
import time

def song_test(song_name):
  """ This function making an HTTP request to route /lyrics, timing the request duration and test if the request is successfull.

  Args:
      song_name (string): song name to search for lyrics

  Raises:
      Exception: HTTP request failed.

  Returns:
      _type_: float (time)
  """
  start = time.time()
  try:
    r = requests.get(f"http://localhost/lyrics?song={song_name}")
  except:
    raise Exception("Something went wrong.")
  end = time.time()
  return end - start

def tests(songs):
  """ This function will loop over songs, and in each iteration it will call the song_test function.

  Args:
      songs (string): list of songs to test

  Raises:
      Exception: Performance was to slow (above 5 seconds).
  """
  for song in songs:
    print(f"Test song: {song}")
    test_no_cache = song_test(song)
    test_with_cache = song_test(song)
    print(f"Duration: {test_with_cache}\n")
    if (test_with_cache > 0.05):
      raise Exception(f"Failed performance test, song request took {test_with_cache}s. The minimum requirment to pass performance test is 0.05s and lower.")

songs_list = ["Halla Madrid", "Toxicity", "Nothing Else Matter", "No woman no cry", "Diary of Jane"]

tests(songs_list)

print("Tests passed successfully :)")

