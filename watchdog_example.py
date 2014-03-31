import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OneDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        print event.src_path
        print 'File created.'

    def on_deleted(self, event):
        print event.src_path
        print 'File deleted.'

    def on_modified(self, event):
        print event.src_path
        print 'File modified.'

    def on_moved(self, event):
        print event.src_path
        print event.dest_path
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
