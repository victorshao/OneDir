import time
import os
import shutil
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import unicodedata
import string
import user
validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

path = 'C:\Users\joyce jian\OneDir\\'
urlprime = 'http://127.0.0.1:5000/'
sync = True
user = "user1"
public = path+"\public"
publicid= "public"
if not os.path.exists(path):
            os.mkdir(path)
            public = path+"/public"
            os.mkdir(public)

class OneDirHandler(FileSystemEventHandler):
    def on_created(self, event):
        url = urlprime +'upload'
        file = None
        if not event.is_directory:
            url += "file/"
            some = event.src_path.replace(path+"\\", '').replace("\\", "/").partition("/")
            if some[0]== publicid:
                url += event.src_path.replace(path +"\\", '').replace(" ", "_").replace("\\", "/")
                files = {'file': open(event.src_path,'r+')}
                r = requests.post(url,files=files)
            else :
                url = url + user
                url += event.src_path.replace(path, '').replace(" ", "_").replace("\\", "/")
                files = {'file': open(event.src_path,'r+')}
                r = requests.post(url,files=files)
            # url = url.replace("uploadfile/","move/")
            # url = url + user
            # url += event.src_path.replace(path, '').replace(" ", "_")
            # r = requests.post(url)
        else:
            url += "/"
            some = event.src_path.replace(path+"\\", '').replace("\\", "/").partition("/")
            if some[0]== publicid:
                url += event.src_path.replace(path+"\\", '').replace(" ", "_").replace("\\", "/") + '/'
                r = requests.post(url)
            else:
                url += user
                url += event.src_path.replace(path, '').replace(" ", "_").replace("\\", "/") + '/'
                r = requests.post(url)

    def on_deleted(self, event):
        url = urlprime+ 'delete/'
        some = event.src_path.replace(path+"\\", '').replace("\\", "/").partition("/")
        if some[0]== publicid:
            url += event.src_path.replace(path+"\\", '').replace(" ", "_").replace("\\", "/")
            r= requests.post(url)
        else:
            files = event.src_path.replace(path,'')
            files = files.replace(" ", "_").replace("\\", "/")
            url += user
            url += files
            r= requests.post(url)

    def on_modified(self, event):
        if not event.is_directory:
            self.on_deleted(event)
            self.on_created(event)


    def on_moved(self, event):
        source = event.src_path #/Home/OneDir/text.txt
        dest = event.dest_path #/Home/OneDir/renamed.txt
        sourcelist = source.split("\\") #remove the file name at the end of the source path
        destlist = dest.split('\\') #remove file name at the end of the dest path
        source = source.replace(sourcelist[len(sourcelist)-1],"")
        dest = dest.replace(destlist[len(destlist)-1], "")

        if source != dest or sourcelist[len(sourcelist)-1] != destlist[len(destlist)-1] :
            url = urlprime+ 'delete/'
            some = event.src_path.replace(path+"\\", '').replace("\\", "/").partition("/")
            if some[0]== publicid:
                url += event.src_path.replace(path+"\\", '').replace(" ", "_").replace("\\", "/")
                r= requests.post(url)
            else:
                files = event.src_path.replace(path,'')
                files = files.replace(" ", "_").replace("\\", "/")
                url += user
                url += files
                r= requests.post(url)
            url = urlprime+'upload'
            file = None
            if not event.is_directory:
                url += "file/"
                some = event.dest_path.replace(path+"\\", '').replace("\\", "/").partition("/")
                if some[0]== publicid:
                    url += event.dest_path.replace(path+"\\", '').replace(" ", "_").replace("\\", "/")
                    files = {'file': open(event.dest_path,'r+')}
                    r = requests.post(url,files=files)
                else :
                    url = url + user
                    url += event.dest_path.replace(path, '').replace(" ", "_").replace("\\", "/")
                    files = {'file': open(event.dest_path,'r+')}
                    r = requests.post(url,files=files)
                # url = url.replace("uploadfile/","move/")
                # url += user
                # url += event.src_path.replace(path, '').replace(" ", "_")
                # r = requests.post(url)
            else:
                url += "/"
                some = event.dest_path.replace(path+"\\", '').replace("\\", "/").partition("/")
                if some[0]== publicid:
                    url += event.dest_path.replace(path+"\\", '').replace(" ", "_").replace("\\", "/") + '/'
                    r = requests.post(url)
                else:
                    url += user
                    url += event.dest_path.replace(path, '').replace(" ", "_").replace("\\", "/") + '/'
                    r = requests.post(url)
                    
def switchsync():
    global sync
    sync = not sync

def download(filename, rootdir=path):
    dirs = filename.split('\\')
    for i in range(len(dirs)-1):
        dirpath = rootdir
        for d in dirs[:i+1]:
            dirpath = os.path.join(dirpath, d)
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
    print filename[-1:]
    if filename[-1:] != '\\':
        r = requests.get(urlprime + 'download/' + filename.replace('\\', '/'))
        with open(os.path.join(rootdir, filename), 'w+') as f:
            f.write(r.content)

#UNTESTED UNTIL HISTORY IS COMPLETE
def startupUpdate():
    #find last time a file was modified
    lastmodified = 0
    for i in os.walk(path):
        for f in path[2]:
            if f[0] != '~': #ignore hidden files
                t = os.path.getmtime(path[0] + '\\' + f)
                if t > lastmodified:
                    lastmodified = t

    #convert timestamp to string in a format sql can handle
    lastmtimestamp = str(datetime.datetime.fromtimestamp(lastmodified))[:23]
    #NEED TO CHECK DATABASE NAME
    download('history.db', os.getcwd())
    conn = sqlite3.connect('history.db')
    to_update = {}
    with conn:
        cur = conn.cursor()
        #NEED TO CHECK TABLE AND COLUMN NAMES
        sql_cmd = 'select * from activitylog where datetime(timestamp) > ?'
        cur.execute(sql_cmd, (lastmtimestamp,))
        while True:
            row = cur.fetchone()
            if row is None:
                break
            #NEED HISTORY FUNCTIONALITY FOR REMAINDER OF CODE


if __name__ == '__main__':
    
    handler = OneDirHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive = True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            # while not sync:
            #     r = raw_input("Type sync to turn on sync ")
            #     if r == "sync":
            #         switchsync()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


