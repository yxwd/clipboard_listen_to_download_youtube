# clipboard_listen_to_download_youtube
Copy the youtube url to  the clipboard，it will be downloaded automatically background，Multithread by python

When i watching the youtube by my windows PC ，I want to download some one of it, I need to copy the url,then use youtube_dl to download it.
Because i need a proxy to view youtube, I will open a command  use a  command line like this:
"youtube-dl --proxy=127.0.0.1:1080 youtube_url"
If there are many video , I need to open many cmd window.

This program is written by Python,it will listen the clipboard,if the clipboard text contain a valid youtube url,it will be download automatically.
It use 3 thread to download,that means you can Download three files at the same time,the other url is in queue,Queue number is 20,you can change it.

In order to use youtube_dl,you should install youtube_dl and "import youtube_dl",and you must download ffmpeg to the same dir.

