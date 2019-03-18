import os
import requests
import json

base_path = "/media/aaron/Elements/ugmo/media/"
# ccc_gtech = ("ccc-gtech", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,396604--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-396604/2142115,2142116,2142117,2142118,2142119,2142120/media_b4744781_", 203)
sbi_ubc_slo = ("sbi-ubc-slo", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,428775--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-428775/2296369,2296370,2296371,2296372,2296373,2296374/media_b4750789_", 351)
sbi_cal_wisco = ("sbi-cal-wisco", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,420688--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-420688/2253335,2253336,2253337,2253338,2253339,2253340/media_b2754149_", 384)
sbi_slo_byu = ("sbi-slo-byu", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,420581--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-420581/2252836,2252837,2252838,2252839,2252840,2252841/media_b1755567_", 250)
sbi_wash_usc = ("sbi-wash-usc", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,428478--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-428478/2294924,2294925,2294926,2294927,2294928,2294929/media_b2751359_", 395)
pres_cal_col = ("pres-cal-col", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,439476--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-439476/2352029,2352030,2352031,2352032,2352033,2352034/media_b4746738_", 319)
pres_ore_slo = ("pres-ore-slo", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,439841--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-439841/2353985,2353986,2353987,2353988,2353989,2353990/media_b4749990_", 282)
pres_ore_ucla = ("pres-ore-ucla", "https://vhx-adaptive-hap.akamaized.net/-ctx--user_id,1948000--platform_id,27--video_id,439477--channel_id,16557--plan,standard-/vods3cf/0/amlst:c-16557/v-439477/2352007,2352008,2352009,2352010,2352011,2352012/media_b4748323_", 230)
ccc_ohio_umass = ("ccc-ohio-umass", "https://12skyfiregce-vimeo.akamaized.net/exp=1551338728~acl=%2F304955211%2F%2A~hmac=1746d6a5379f423ae95da3721d8996d8963d8f25250679467337d45898d907c0/304955211/video/1169237046/chop/segment-", 149)
ccc_ohio_mich = ("ccc-ohio-mich", "https://skyfire.vimeocdn.com/1551339224-0xaa94c075e18882b5f567483977eef9c34974d278/305330500/video/1170938652/chop/segment-", 269)
fw_byu_nwst = ("fw-byu-nwst", "https://112skyfiregce-vimeo.akamaized.net/exp=1551340147~acl=%2F317323711%2F%2A~hmac=6009496b1648ce414b0ced57bf0aa0e8077e5713b283907614080ae3c77c7e88/317323711/video/1228938607/chop/segment-", 295)
cci_pitt_umass =("cci-pitt-umass", "https://48skyfiregce-vimeo.akamaized.net/exp=1552623361~acl=%2F323321247%2F%2A~hmac=53c4e4c79cb615dd695b055ef9dbca59e5d2b5d42800a1813eafe552eaa59109/323321247/video/1258868800/chop/segment-", 305)

class Game:
    def __init__(self, p, n, u, s):
        self.path = p
        self.name = n
        self.url = u
        self.segments = s
        self.full_path = self.path + "/" + self.name


def create():
    file_name= raw_input("Folder and file name (eg: pres-cal-col): ")
    path = os.path.abspath("/media/aaron/Elements/ugmo/media/")
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
# ffmpeg -i INPUT.ts -acodec copy -vcodec copy -bsf:a aac_adtstoasc OUTPUT.mp4


