import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OneDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        pos = event.src_path.find('OneDir')
        path = event.src_path[:pos] + 'TwoDir' + event.src_path[pos+6:]
        if event.is_directory:
            shutil.copytree(event.src_path, path)
        else:
            shutil.copy(event.src_path, path)
        print 'File created.'

    def on_deleted(self, event):
        pos = event.src_path.find('OneDir')
        path = event.src_path[:pos] + 'TwoDir' + event.src_path[pos+6:]
        print path
        print event.is_directory
        if event.is_directory:
            shutil.rmtree(path)
        else:
            os.remove(path)
        print 'File deleted.'

    def on_modified(self, event):
        if not event.is_directory:
            pos = event.src_path.find('OneDir')
            path = event.src_path[:pos] + 'TwoDir' + event.src_path[pos+6:]
            shutil.copy(event.src_path, path)
        print 'File modified.'

    def on_moved(self, event):
        pos = event.src_path.find('OneDir')
        spath = event.src_path[:pos] + 'TwoDir' + event.src_path[pos+6:]
        dpath = event.dest_path[:pos] + 'TwoDir' + event.dest_path[pos+6:]
        os.rename(spath, dpath)
        print 'File moved.'

if __name__ == '__main__':
    path = 'C:\Users\joyce jian\OneDir'
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

