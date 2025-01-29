import json

def parse_har_file(filename):
  with open(filename + ".har", 'r') as f:
    har_data = json.load(f)

  prev_number = 0;

  url_file = open(filename + "_urls.txt", "a")
  for entry in har_data['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    status_code = entry['response']['status']
    if ".ts?skid" in url:
        if status_code != 200:
          print(f"Status: {status_code}, URL: {url}")
        url_file.write(url)
        url_file.write("\n")
  url_file.close()
