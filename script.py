import os
import requests
import json

class Game:
    def __init__(self, p, n, u, s):
        self.path = p
        self.name = n
        self.url = u
        self.segments = s
        self.full_path = self.path + "/" + self.name

def create():
    file_name= raw_input("Folder and file name (eg: pres-cal-col): ")
    path = os.path.abspath("/media/aaron/Elements/ugmo/media/") # DEFAULT
    while True:
        new_path = raw_input("Path (default is \'" + path + "\'): ")
        if new_path == "":
            print("Sticking with default path.")
            break
        elif os.path.exists(new_path):
            path = new_path
            break
        else:
            print("Please enter a valid path.")
    print("Path to folder will be \'" + path + "/" + file_name +"\'")
    url = raw_input("Paste url without the ###.ts: ")
    segments = 0
    while True:
        segments = raw_input("Number of segments: ")
        if segments.isdigit() and int(segments) > 0:
            segments = int(segments)
            break
        else:
            print("Not a number.")
    return Game(path, file_name, url, segments)


def get_requests(game):
    path = game.full_path
    if not os.path.exists(path):
        print ("\'" + path + "\' does not currently exist.")
        print("Creating now...")
        os.mkdir(path)
    request_pre_str = game.url
    request_post_str = ".ts"
    for i in range(1, game.segments + 1):
        request_str = request_pre_str + str(i) + request_post_str
        download_video(request_str, path, str(i) + ".ts")
    print("Done downloading.")

def download_video(request_str, save_to_dir, filename):
    request = requests.get(request_str, stream=True)
    if request.status_code == 200:
        print("Downloading clip", filename)
    else:
        print("Failed. Status_code=" + request.status_code)
        return
    with open(os.path.join(save_to_dir, filename), "wb") as f:
        # print('Dumping "{0}"...'.format(filename))
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        print("Done with", filename)

def merge_ts(path, num_files):
    for i in range(1, num_files + 1):
        with open(os.path.join(path, "full.ts"), "ab") as outfile:
            with open(os.path.join(path, str(i) + ".ts"), "rb") as infile:
                outfile.write(infile.read())
                print("Done reading from file", str(i) + ".ts")
    print("Done merging ts")

game = create()
get_requests(game)
merge_ts(game.full_path, game.segments)
print("=======DONE=======")
print("Run the following two commands.")
print("cd " + game.full_path)
print("ffmpeg -i full.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc " + game.name + ".mp4")
print("OR")
print("ffmpeg -i " + game.full_path + "/full.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc " + game.full_path + "/" + game.name + ".mp4")
# ffmpeg -i INPUT.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc OUTPUT.mp4
