#!/usr/bin/env python
import sys
import os
import time
import logging
import pwd
import grp
from watchdog import events
from watchdog.events import DirCreatedEvent
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Environment():
    def __init__(self):
        try:
            self.dirperms = int(os.environ['DIRPERMS'], 8)
        except Exception as e:
            self.dirperms = int('0777', 8)
        try:
            self.diruser = os.environ['DIRUSER']
        except Exception as e:
            self.diruser = None
        try:
            self.dirgroup = os.environ['DIRGROUP']
        except Exception as e:
            self.dirgroup = None
        try:
            self.fileperms = int(os.environ['FILEPERMS'], 8)
        except Exception as e:
            self.fileperms = int('0664', 8)
        try:
            self.fileuser = os.environ['FILEUSER']
        except Exception as e:
            self.fileuser = None
        try:
            self.filegroup = os.environ['FILEGROUP']
        except Exception as e:
            self.filegroup = None


class MyHandler(events.FileSystemEventHandler):
    def on_created(self, event):
        perms = Environment()
        msg = []
        if type(event) == events.DirCreatedEvent:
            try:
                msg.append('Directory {} created.'.format(event.src_path))
                os.chmod(event.src_path, perms.dirperms)
                msg.append('Changed perms to {}.'.format(oct(perms.dirperms)))
                if perms.diruser or perms.dirgroup:
                    if not perms.diruser:
                        uid = os.stat(event.src_path).st_uid
                    else:
                        uid = pwd.getpwnam(perms.diruser).pw_uid
                        msg.append('Changed user to {}.'.format(perms.diruser))
                    if not perms.dirgroup:
                        gid = os.stat(event.src_path).st_uid
                    else:
                        gid = grp.getgrnam(perms.dirgroup).gr_gid
                        msg.append(
                            'Changed group to {}.'.format(perms.dirgroup))
                    os.chown(event.src_path, uid, gid)
                logging.info(' '.join(msg))
            except Exception as e:
                print type(e)
                print e
                msg = "Error while changing permissions to {}".format(
                    event.src_path)
                logging.error(msg)
        if type(event) == events.FileCreatedEvent:
            try:
                msg.append('File {} created.'.format(event.src_path))
                os.chmod(event.src_path, perms.fileperms)
                msg.append('Changed perms to {}.'.format(oct(perms.fileperms)))
                if perms.fileuser or perms.filegroup:
                    if not perms.fileuser:
                        uid = os.stat(event.src_path).st_uid
                    else:
                        uid = pwd.getpwnam(perms.fileuser).pw_uid
                        msg.append("Changed user to {}.".format(perms.fileuser))
                    if not perms.filegroup:
                        gid = os.stat(event.src_path).st_uid
                    else:
                        gid = grp.getgrnam(perms.filegroup).gr_gid
                        msg.append(
                            "Changed group to {}.".format(perms.filegroup))
                    os.chown(event.src_path, uid, gid)
                logging.info(' '.join(msg))
            except Exception as e:
                print type(e)
                print e
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
