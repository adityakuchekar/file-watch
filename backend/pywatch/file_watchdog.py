import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

dir_to_watch = "/home/aditya/aditya_kuchekar/watchdog"


def get_name(string):
    return string.split("/")[-1]


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory


    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        # try:
        #     while True:
        #         time.sleep(1)
        # except:
        #     self.observer.stop()
        # self.observer.join()
        # print("\nWatcher Terminated\n")


class MonitorFolder(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_created(self, event):
        self.queue.append({
            "event_type": event.event_type,
            "src_path": event.src_path,
            "file_name": get_name(event.src_path),
            "is_directory": event.is_directory
        })

    def on_deleted(self, event):
        self.queue.append({
            "event_type": event.event_type,
            "src_path": event.src_path,
            "file_name": get_name(event.src_path),
            "is_directory": event.is_directory
        })

    # def on_moved(self, event):
    #     self.queue.append({
    #         "event_type": event.event_type,
    #         "src_path": event.src_path,
    #         "dest_path": event.dest_path,
    #         "is_directory": event.is_directory
    #     })


def get_watcher(directory, queue):
    # w = Watcher("/home/aditya/aditya_kuchekar/watchdog", MonitorFolder())
    w = Watcher(directory=directory, handler=MonitorFolder(queue))
    w.run()


if __name__ == "__main__":
    get_watcher(dir_to_watch, [])

