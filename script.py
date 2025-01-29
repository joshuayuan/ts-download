import os
import pathlib
import requests
import json
from tqdm import tqdm
from http.cookiejar import MozillaCookieJar
from har_parser import parse_har_file

cookiesFile = str(pathlib.Path(__file__).parent.absolute() / "ultiworld-cookies.txt")  # Places "cookies.txt" next to the script file.
cj = MozillaCookieJar(cookiesFile)
if os.path.exists(cookiesFile):  # Only attempt to load if the cookie file exists.
    cj.load(ignore_discard=True, ignore_expires=True)  # Loads session cookies too (expirydate=0).
s = requests.Session()
s.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept-Language": "en-US,en"
}
s.cookies = cj  # Tell Requests session to use the cookiejar.

class Video:
    """
    option 1
    """
    def __init__(self, p, n, up, um, us, s):
        self.option = 1
        self.path = p
        self.name = n
        self.url_prefix = up
        self.url_mid= um
        self.url_suffix = us
        self.segments = s
        self.full_path = self.path + "/" + self.name
        self.temp_path = self.full_path + "_TEMP" # temporary folder

    """
    option 2
    """
    def __init__(self, p, n, h, s):
        self.option = 2
        self.path = p
        self.name = n
        self.har_file_name = h
        self.segments = s
        self.full_path = self.path + "/" + self.name
        self.temp_path = self.full_path + "_TEMP" # temporary folder

def create():
    option = int(input("Enter 1 if you want to scrape directly from the link, and enter 2 if you want to scrape from a .har file: ").strip())
    file_name= input("File name (don't include the extension): ").strip()
    # FILL THIS WITH YOUR OWN DEFAULT PATH
    path = os.path.abspath("")
    while True:
        new_path = input("Path (default is \'" + path + "\'): ")
        if new_path == "":
            print("Sticking with default path.")
            break
        elif os.path.exists(new_path):
            path = new_path
            break
        else:
            print("Please enter a valid path.")
    print("Path to output files will be \'" + path + "/" + file_name +"..\'")
    if option == 1:
        url_prefix = input("Paste url prefix without '###.ts': ").strip()
        url_mid = input("Paste anything between the ## and .ts: ").strip()
        url_suffix = input("Paste url suffix: ").strip()
        segments = 0
        while True:
            segments = input("Number of segments: ")
            if segments.isdigit() and int(segments) > 0:
                segments = int(segments)
                break
            else:
                print("Not a valid number.")

        return Video(path, file_name, url_prefix, url_mid, url_suffix, segments)

    elif option == 2:
        har_file_name = input("File name of har file without extension: ").strip()
        if "." in har_file_name:
          har_file_name = input("Please do not include extensions. Please try again: ").strip()
        parse_har_file(har_file_name)
        segments = 0
        while True:
            segments = input("Number of segments: ")
            if segments.isdigit() and int(segments) > 0:
                segments = int(segments)
                break
            else:
                print("Not a valid number.")

        return Video(path, file_name, har_file_name, segments)

    print("Error creating video object.")
    return


def get_requests(video):
    path = video.temp_path
    if os.path.exists(path):
        print ("\'" + path + "\' currently exist.")
        return
    else:
        print ("Creating \'" + path + "\'")
        os.mkdir(path)
    if video.option == 1:
        request_pre_str = video.url_prefix
        request_post_str = video.url_mid + ".ts" + video.url_suffix
        for i in tqdm(range(1, video.segments + 1)):
            request_str = request_pre_str + str(i) + request_post_str
            if i == 1:
                print(request_str)
            download_video(request_str, path, str(i) + ".ts")
    elif video.option == 2:
        urls = open(video.name + "_urls.txt", "r")
        for i in tqdm(range(1, video.segments + 1)):
            download_video(urls.readline(), path, str(i) + ".ts")

    print("Done downloading.")

def download_video(request_str, save_to_dir, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    try:
        response = s.get(request_str, stream=True)
    except:
        print("Failing on: ", requests.request)
        return
    if response.status_code != 200:
        # print("Downloading clip", filename)
    # else :
        print("Failed. Status_code=", response.status_code)
        return
    with open(os.path.join(save_to_dir, filename), "wb") as f:
        # print('Dumping "{0}"...'.format(filename))
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        # print("Done with", filename)

def merge_ts(path, num_files):
    for i in tqdm(range(1, num_files + 1)):
        with open(os.path.join(path, "full.ts"), "ab") as outfile:
            with open(os.path.join(path, str(i) + ".ts"), "rb") as infile:
                outfile.write(infile.read())
                # print("Done reading from file", str(i) + ".ts")
    print("Done merging ts")

video = create()
get_requests(video)
merge_ts(video.temp_path, video.segments)
print("=======DONE=======")
print("Run the following two commands.")
print("cd " + video.temp_path)
print("ffmpeg -i full.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc " + video.name + ".mp4")
print("OR")
print("ffmpeg -i " + video.temp_path + "/full.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc " + video.full_path + ".mp4")
print("rm -rf " + video.temp_path)
# ffmpeg -i INPUT.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc OUTPUT.mp4
