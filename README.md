## How to use ##
there are 2 options.
Option 1 is outdated but originally, you could just take the url and change the .ts prefix, and so we'd just generate all the requests and go from there.
Option 2 now requires you to use a .har file which is the export from chrome dev tools network tool. So I play the full video in the background, fastforwarding when possible, so that the video player is generating all those requests that each have unique signatures attached in the request url. Then i export the the har file which has those urls, and that's what i download here.

run `python3 script.py` and follow the instructions. Lots of edge  cases are not caught!

## TODO ##
- delete ts and temporary files
- implement ffmpeg in code
- support for windows and mac
- GUI
- just take url of page, and search network ourselves
- throw it all into an web tool
