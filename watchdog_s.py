import time
import os
import shutil
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OneDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        url = 'http://127.0.0.1:5000/upload'
        files = {'file': open(event.src_path,'r+')}
        r = requests.post(url,files=files)


    # def on_deleted(self, event):
    #
    #
    # def on_modified(self, event):
    #
    #
    # def on_moved(self, event):


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