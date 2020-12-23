import youtube_dl
import os
import win32clipboard
import win32con
#pip install pywin32
import re
import queue
import threading
import time

exitFlag = 0
def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(0)
    else:
        return "0"

    #return youtube_regex_match
def clipboard_clear():
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
    except Exception as e:
        print('Error in clear ')
        print(e)
    finally:
        win32clipboard.CloseClipboard()

def clipboard_get():
    global exitFlag
    youtube_url='0'
    try:
        win32clipboard.OpenClipboard()
        src_url= win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        if src_url=='quit':
            youtube_url=src_url
        else:
            youtube_url=youtube_url_validation(src_url)
        if youtube_url!='0':
           win32clipboard.EmptyClipboard() 
    except Exception as e:
        pass
    finally:
        win32clipboard.CloseClipboard()



    return youtube_url

def my_hook(d):

    if d['status'] == 'finished':
        #stop_flag=1
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {} ,now converting ...".format(file_tuple[1]))
        print(d)
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'videoformat' : "mp4",
    'writethumbnail': False,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': 'en',
    'noplaylist' : True,
    'nopart': True,
    'progress_hooks': [my_hook],
    'proxy':'127.0.0.1:1080',
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
}


class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("Begin thread ：" + self.name)
        process_data(self.name, self.q)
        print ("Exiting thread：" + self.name)

def process_data(threadName, q):
    global max_retry,exitFlag
    infoflag=False
    title=''
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            youtube_url = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, youtube_url))
            n=0
            stop_flag=0
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                while n<max_retry:
                    try:
                        if stop_flag==1:
                            break
                        if exitFlag:
                            break
                        if infoflag==False:
                            info = ydl.extract_info(youtube_url)
                            infoflag=True
                            title=info['title']
                            print("%s begin to download  %s" %(threadName,title))
                        ydl.download([youtube_url])
                        stop_flag=1
                    except Exception as e:
                        print(e)

                        print("%s retry to download %s (%d/%d)" %(threadName,title,n+1,max_retry))
                        n=n+1
                        stop_flag=0
            print ("%s processed done" % (threadName))
        else:
            queueLock.release()
        time.sleep(1)
#https://www.youtube.com/watch?v=AijYVLi4F9I
threadList = ["Thread-1", "Thread-2", "Thread-3"]
queueLock = threading.Lock()
workQueue = queue.Queue(20)
threads = []
threadID = 1
max_retry=100


# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
print("Begin to listen the clipboard")
# 填充队列


recent_txt='0'
while True:
    # txt 存放当前剪切板文本
    txt = clipboard_get()
    if txt=='quit':

        exitFlag = 1
    if exitFlag:
        break
    if txt!='0' and txt!=recent_txt:
        recent_txt=txt
        queueLock.acquire()
        print(txt)
        workQueue.put(txt)
        queueLock.release()
    time.sleep(1)
# 等待队列清空
#while not workQueue.empty():
#    pass
# 通知线程是时候退出
print("Waiting thread to exit")


# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

quit()



print(clipboard_get())

