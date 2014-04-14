import time
import os
import shutil
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import unicodedata
import string
validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
def removeDisallowedFilenameChars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

class OneDirHandler(FileSystemEventHandler):
    def on_created(self, event):
        url = 'http://127.0.0.1:5000/upload'
        file = None
        try:
            files = {'file': open(event.src_path,'r+')}
            r = requests.post(url,files=files)
        except IOError:
            print 'Folder object created'



    def on_deleted(self, event):
        url = 'http://127.0.0.1:5000/delete/'
        files = os.path.basename(event.src_path)
        files = removeDisallowedFilenameChars(files)
        files = files.replace(" ", "_")
        url=url+files
        r= requests.post(url)

    def on_modified(self, event):
        self.on_deleted(event)
        self.on_created(event)


    def on_moved(self, event):
        source = event.src_path #/Home/OneDir/text.txt
        dest = event.dest_path #/Home/OneDir/renamed.txt
        sourcelist = source.split("\\") #remove the file name at the end of the source path
        destlist = dest.split('\\') #remove file name at the end of the dest path
        source = source.replace(sourcelist[len(sourcelist)-1],"")
        dest = dest.replace(destlist[len(destlist)-1], "")
        print destlist[len(destlist)-1]

        if source != dest or sourcelist[len(sourcelist)-1] != destlist[len(destlist)-1] :
            url = 'http://127.0.0.1:5000/delete/'
            files = os.path.basename(event.src_path)
            files = removeDisallowedFilenameChars(files)
            files = files.replace(" ", "_")
            url=url+files
            r= requests.post(url)
            url = 'http://127.0.0.1:5000/upload'
            file = None
            try:
                files = {'file': open(event.dest_path,'r+')}
                r = requests.post(url,files=files)
            except IOError:
                print 'Folder object created'


if __name__ == '__main__':
    path = 'C:\Users\PShao\Pictures\stuff\manga'
    handler = OneDirHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive = True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()