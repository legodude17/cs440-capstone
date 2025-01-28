import html
import html.parser
import urllib3
import tarfile
import os
import pandas as pd

BASE_URL = "http://arimaa.com/arimaa/download/gameData/"

html_urls = [BASE_URL]
archive_urls = []

http = urllib3.PoolManager()

cur_url = BASE_URL

class MyHTMLParser(html.parser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value != None:
                    # If we find a link, it's either a subfolder or an archive
                    if value.endswith("/"):
                        # Subfolders we add to the list to be explored
                        html_urls.append(cur_url + value)
                    elif value.endswith(".tgz"):
                        # Archives we add to that link
                        archive_urls.append(cur_url + value)

# We treat the html_urls list like a queue
while len(html_urls) > 0:
  cur_url = html_urls.pop()
  resp = http.request("GET", cur_url)
  p = MyHTMLParser()
  p.feed(str(resp.data))
  p.close()

if not os.access("games", os.R_OK):
  os.mkdir("games")

# Download and extract all the archives
for url in archive_urls:
  print("Downloading", url)
  resp = http.request("GET", url, preload_content=False)
  z = tarfile.open("games", "r", resp) # type: ignore
  z.extractall("games")
  z.close()

# This file is redudant
os.remove("games/allgames2006.txt")

# These two don't have the game data I need
os.remove("games/ratedgames.txt")
os.remove("games/eventgames.txt")

def read_file(path):
  """
  Read a games file and create a table with only the relevant columns
  """
  print("Reading", path)
  try:
    t = pd.read_table("games/" + path, usecols=["result", "movelist"])
  except UnicodeDecodeError:
    print("  Invalid encoding...")
    os.remove("games/" + path)
    raise ValueError("Failed to read from " + path)
  return t


# Create a list of all the tables from the games folder,
# with only the relevant columns

files = os.listdir("games")
tables = []

for file in files:
  try:
    tables.append(read_file(file))
  except ValueError:
    pass

# Concatenate all the tables and write them to a single file

table = pd.concat(tables, axis=0, copy=False)

print("Writing allgames.txt")
table.to_csv("allgames.txt", index=False)
