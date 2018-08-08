#!/usr/bin/env python
import sys
import os
import time
import logging
from watchdog import events
from watchdog.events import DirCreatedEvent
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

try: 
    perms = int(os.environ['PERMS'], 8)
except Exception as e:
    perms = int('0777', 8)

class MyHandler(events.FileSystemEventHandler):
    def on_created(self, event):
        if type(event) == events.DirCreatedEvent:
            try:
                os.chmod(event.src_path, perms)
                msg = "Directory {} created. Changed perms to {}.".format(
                    event.src_path, oct(perms))
                logging.info(msg)
            except Exception as e:
                msg = "Error while changing permissions to {}".format(
                    event.src_path)
                logging.error(msg)


def main():
    try:
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    except OSError as e:
        msg = "{} is not a directory.".format(sys.argv[1])
        print msg


if __name__ == "__main__":
    main()
