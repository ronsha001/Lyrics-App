import requests
import time

def song_fail(link):
  """ This function is called for a link that supposed to fail and return an error

  Raises:
      Exception: if get request not failing, then raise exception
  """

  try:
    r = requests.get(link)
    print(f"Designated Failure Link: {link}, Error: {r.text}")
  except Exception as err:
    if err != "Something went wrong! Error: no language or song name specified":
      raise Exception("Failing test doesn't throw an exception!")

def song_test(song):
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
    r = requests.get(f"http://localhost/lyrics?song={song['song_name']}&lang={song['language']}")
  except:
    raise Exception("Something went wrong.")
  end = time.time()
  return end - start

def tests(songs, designated_failure_links):
  """ This function will loop over songs, and in each iteration it will call the song_test function.

  Args:
      songs (string): list of songs to test

  Raises:
      Exception: Performance was to slow (above 5 seconds).
  """
  for song in songs:
    print(f"Test song: {song}")
    test_without_cache = song_test(song)
    test_with_cache = song_test(song)
    print(f"Duration: {test_with_cache}\n")
    if (test_with_cache > 0.05):
      raise Exception(f"Failed performance test, song request took {test_with_cache}s. The minimum requirment to pass performance test is 0.05s and lower.")

  for link in designated_failure_links:
    song_fail(link)


songs_list = [
              {"song_name": "Halla Madrid", "language": "en"},
              {"song_name": "Toxicity", "language": "en"},
              {"song_name": "Nothing Else Matter", "language": "en"},
              {"song_name": "No woman no cry", "language": "en"},
              {"song_name": "Diary of Jane", "language": "en"},
              {"song_name": "Halla Madrid", "language": "en"},
              {"song_name": "Eyal Golan Yafa Sheli", "language": "he"}
            ]

designated_failure_links = [
                            "http://localhost/lyrics?song=hello",
                            "http://localhost/lyrics?lang=he",
                            "http://localhost/lyrics?lang=lo",
                            "http://localhost/lyrics"
                          ]

tests(songs_list, designated_failure_links)

print("Tests passed successfully :)")

