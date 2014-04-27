import time
import os
import shutil
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import string
import user
import sys
import datetime
import sqlite3
import music

path = os.path.expanduser('~/onedir')
urlprime = 'http://127.0.0.1:5000/'
public = path+"/public"
publicid= "public"
if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir(public)

class watcher:
    global urlprime
    global publicid
    global path
    sync = True
    user = None

    def __init__(self, user2, prime):
        global user
        global urlprime
        urlprime = prime
        user = user2.get_user_id()
        start = music.start()


    class OneDirHandler(FileSystemEventHandler):

        def on_created(self, event):
            global urlprime
            global publicid
            global path
            url = urlprime +'upload'
            file = None
            if not event.is_directory:
                url += "file/"
                some = event.src_path.replace(path+"/", '').partition("/")
                if some[0]== publicid:
                    url += event.src_path.replace(path +"/", '')
                    files = {'file': open(event.src_path,'r+')}
                    r = requests.post(url,files=files)
                else :
                    url = url + user
                    url += event.src_path.replace(path+"/", '')
                    files = {'file': open(event.src_path+"/",'r+')}
                    r = requests.post(url,files=files)
                # url = url.replace("uploadfile/","move/")
                # url = url + user
                # url += event.src_path.replace(path, '').replace(" ", "_")
                # r = requests.post(url)
            else:
                url += "/"
                some = event.src_path.replace(path+"/", '').partition("/")
                if some[0]== publicid:
                    url += event.src_path.replace(path+"/", '') + '/'
                    r = requests.post(url)
                else:
                    url += user
                    url += event.src_path.replace(path+"/", '') + '/'
                    r = requests.post(url)

        def on_deleted(self, event):
            global urlprime
            global publicid
            global path
            url = urlprime+ 'delete/'
            some = event.src_path.replace(path+"/", '').partition("/")
            if some[0]== publicid:
                url += event.src_path.replace(path+"/", '')
                r= requests.post(url)
            else:
                files = event.src_path.replace(path+"/",'')
                url += user
                url += files
                r= requests.post(url)

        def on_modified(self, event):
            global urlprime
            global publicid
            global path
            if not event.is_directory:
                self.on_deleted(event)
                self.on_created(event)


        def on_moved(self, event):
            global urlprime
            global publicid
            global path
            source = event.src_path #/Home/OneDir/text.txt
            dest = event.dest_path #/Home/OneDir/renamed.txt
            sourcelist = source.split("/") #remove the file name at the end of the source path
            destlist = dest.split('/') #remove file name at the end of the dest path
            source = source.replace(sourcelist[len(sourcelist)-1],"")
            dest = dest.replace(destlist[len(destlist)-1], "")

            if source != dest or sourcelist[len(sourcelist)-1] != destlist[len(destlist)-1] :
                url = urlprime+ 'delete/'
                some = event.src_path.replace(path+"/", '').partition("/")
                if some[0]== publicid:
                    url += event.src_path.replace(path+"/", '')
                    r= requests.post(url)
                else:
                    files = event.src_path.replace(path+"/",'')
                    url += user
                    url += files
                    r= requests.post(url)
                url = urlprime+'upload'
                file = None
                if not event.is_directory:
                    url += "file/"
                    some = event.dest_path.replace(path+"/", '').partition("/")
                    if some[0]== publicid:
                        url += event.dest_path.replace(path+"/", '')
                        files = {'file': open(event.dest_path,'r+')}
                        r = requests.post(url,files=files)
                    else :
                        url = url + user
                        url += event.dest_path.replace(path+"/", '')
                        files = {'file': open(event.dest_path,'r+')}
                        r = requests.post(url,files=files)
                    # url = url.replace("uploadfile/","move/")
                    # url += user
                    # url += event.src_path.replace(path, '').replace(" ", "_")
                    # r = requests.post(url)
                else:
                    url += "/"
                    some = event.dest_path.replace(path+"/", '').partition("/")
                    if some[0]== publicid:
                        url += event.dest_path.replace(path+"/", '')+ '/'
                        r = requests.post(url)
                    else:
                        url += user
                        url += event.dest_path.replace(path+"/", '') + '/'
                        r = requests.post(url)

    def switchsync(self):
        global sync
        sync = not sync

    #'filename' is the path to the file to be downloaded
    #'rootdir' is the directory where the file will be downloaded
    def download(self, filename, rootdir=path):
        #create directories the file should be in
        dirs = filename.split('/')
        for i in range(len(dirs)-1):
            dirpath = rootdir
            for d in dirs[:i+1]:
                dirpath = os.path.join(dirpath, d)
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
        #actually download file, if it is one
        if filename[-1:] != '/':
            r = requests.get(urlprime + 'download/' + filename)
            with open(os.path.join(rootdir, filename), 'w+') as f:
                f.write(r.content)

    #UNTESTED
    def startupUpdate(self):
        #find last time a file was modified
        lastmodified = 0
        for i in os.walk(path):
            for f in path[2]:
                if f[0] != '~': #ignore hidden files
                    t = os.path.getmtime(path[0] + '/' + f)
                    if t > lastmodified:
                        lastmodified = t

        #convert timestamp to string in a format sql can handle
        lastmtimestamp = str(datetime.datetime.fromtimestamp(lastmodified))[:23]
        #NEED TO CHECK DATABASE NAME
        self.download('history.db', os.getcwd())
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
                to_update[row[0]] = row[1]

        for f in to_update:
            if to_update[f] == 'delete':
                p = os.path.join(path, f)
                #have to change this section to work for directories
                if os.path.exists(p):
                    os.remove(p)
            else:
                self.download(f, path)

    def main(self):
        while not user == None:
            handler = self.OneDirHandler()
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
    def halt(self):
        # exit = music.exit()
        sys.exit(0)


if __name__ == "__main__":
    user1 = user.user()
    user1.set_user_id("abs")
    watch = watcher(user1, 'http://127.0.0.1:5000/')
    watch.main()
