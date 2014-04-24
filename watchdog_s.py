import time
import os
import shutil
import requests
import unicodedata
import string
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

path = 'C:\Users\PShao\Desktop\New folder'
urlprime = 'http://127.0.0.1:5000/'
sync = True
user = "user1"

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
            url += user
            url += event.src_path.replace(path, '').replace(" ", "_").replace("\\", "/") + '/'
            r = requests.post(url)

    def on_deleted(self, event):
        url = urlprime+ 'delete/'
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
            files = event.src_path.replace(path,'').replace("\\", "/")
            files = files.replace(" ", "_")
            url += user
            url=url+files
            r= requests.post(url)
            url = urlprime+'upload'
            file = None
            if not event.is_directory:
                url += "file/"
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
                url += user
                url += event.dest_path.replace(path, '').replace(" ", "_").replace("\\", "/") + '/'
                r = requests.post(url)
                
def switchsync():
    global sync
    if sync:
        sync = False
    else:
        sync = True

def download(filename):
    r = requests.get(urlprime + 'download/' + filename)
    with open(filename, 'w+') as f:
        f.write(r.content)
        

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


