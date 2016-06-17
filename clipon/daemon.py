#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import time
import os
import fcntl
import json
import threading
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Gdk, GObject
from history import ClipHistory, ClipEntry
from helper import init_log, logger, INT_MAX
from defines import *

def clipon_dbus_method(name):
    return (CLIPON_BUS_NAME + '.' +  name)

"""
Clipon daemon creates two threads. One for monitoring
the clipboard change and save the clipboard content.
Another one for servicing requests from clients through
DBus mechanism.
"""

class CliponConfig():
    """
    Manage clipon configurations
    """
    cfg = {
        'autosave': True,
        'max_entry':INT_MAX,
        'max_length':INT_MAX
        }

    table = {}
    cfg_file = None

    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        pass

    def set_value(self, key, value):
        self.cfg[key] = value
        self.save()

    def get_value(self, key):
        return self.cfg.get(key, None)

    def set_method(self, key, method):
        self.table[key] = method

    def get_method(self, key):
        return self.table.get(key, None)

    def load(self):
        path = self.cfg_file
        if not os.path.isfile(path):
            fd = open(path, 'w', encoding='utf-8')
            json.dump(self.cfg, fd)
            return

        fd = open(path, encoding='utf-8')
        cfg = json.load(fd)
        logger.info("Loaded cfg:\n" + str(cfg))
        for k, v in cfg.items():
            self.cfg[k] = v

    def save(self):
        path = self.cfg_file
        fd = open(path, 'w', encoding='utf-8')
        json.dump(self.cfg, fd)
        logger.info("Saved cfg:\n" + str(self.cfg))

class ClipboardMonitor(threading.Thread):
    """
    Monitor the change of clipboard and save the content
    """
    clipboard = None
    history = None
    paused = False

    def __init__(self, history):
        threading.Thread.__init__(self)
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.history = history

    def stop(self):
        Gtk.main_quit()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):
        logger.info("Clipboard monitor started")
        self.clipboard.connect('owner-change', self.check_clipboard)
        Gtk.main()

    def check_clipboard(self, *args):
        if self.paused:
            return

        text = self.clipboard.wait_for_text()
        self.history.add_text(text)

class CliponDaemon(threading.Thread, dbus.service.Object):
    """
    Daemon for servicing requests from clients through
    DBus communication
    """
    history = None
    cfg_file = None #clipon configure file
    monitor = None
    main_loop = None
    status = 'inactive'
    cfg = None
    log_file = None
    lockf = None

    def __init__(self):
        threading.Thread.__init__(self)

    def setup(self):
        self.cfg_dir = GLib.get_user_config_dir()
        self.cfg_dir = os.path.join(self.cfg_dir, 'clipon')
        self.cfg_file = os.path.join(self.cfg_dir, 'clipon.conf')
        if not os.path.exists(self.cfg_dir):
            os.mkdir(self.cfg_dir, 0o700)

        data_dir = GLib.get_user_data_dir()
        data_dir = os.path.join(data_dir, 'clipon')
        self.log_file = os.path.join(data_dir, 'clipon.log')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir, 0o700)

        init_log(self.log_file)

    def run(self):

        #lock a tmp file to avoid starting multiple daemons
        self.lockf = open('/tmp/clipon-lock', 'w')
        try:
            fcntl.flock(self.lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            logger.error("Unable to lock file")
            return

        self.setup()

        self.cfg = CliponConfig(self.cfg_file)
        self.cfg.load()
        self.cfg.save()

        self.history = ClipHistory(self.cfg)

        self.monitor = ClipboardMonitor(self.history)
        self.monitor.start()

        dbus_loop = DBusGMainLoop()
        bus_name = dbus.service.BusName(CLIPON_BUS_NAME,
                        bus=dbus.SessionBus(mainloop=dbus_loop))
        dbus.service.Object.__init__(self, bus_name,
                                     CLIPON_OBJ_PATH)

        GObject.threads_init() #should be called before mainloop
        self.main_loop = GObject.MainLoop()

        self.status = 'active'
        try:
            logger.info("DBus service started")
            self.main_loop.run()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    @dbus.service.method(clipon_dbus_method('stop'))
    def stop(self):
        self.monitor.stop()
        self.main_loop.quit()
        fcntl.flock(self.lockf, fcntl.LOCK_UN)
        logger.info("DBus service stopped")

    @dbus.service.method(clipon_dbus_method('pause'))
    def pause(self):
        self.status = 'inactive'
        self.monitor.pause()
        logger.info("Paused clipboard monitor")

    @dbus.service.method(clipon_dbus_method('resume'))
    def resume(self):
        self.status = 'active'
        self.monitor.resume()
        logger.info("Resumed clipboard monitor")

    @dbus.service.method(clipon_dbus_method('get_clip_entry'))
    def get_clip_entry(self, index):
        entry = self.history.get_entry(index)
        if entry is not None:
            return json.dumps(entry.info())
        else:
            return None

    @dbus.service.method(clipon_dbus_method('del_history'))
    def del_history(self, start, end):
        return self.history.del_range(start, end)

    @dbus.service.method(clipon_dbus_method('clear_history'))
    def clear_history(self):
        return self.history.clear()

    @dbus.service.method(clipon_dbus_method('history_size'))
    def history_size(self):
        return self.history.size()

    @dbus.service.method(clipon_dbus_method('save_history'))
    def save_history(self):
        return self.history.save()

    @dbus.service.method(clipon_dbus_method('get_info'))
    def get_info(self):
        info = {}
        history_info = self.history.info()
        info['Status'] = self.status
        info['Configure file'] = self.cfg_file
        info['History Info'] = history_info
        info['Log file'] = self.log_file
        return json.dumps(info)

    @dbus.service.method(clipon_dbus_method('get_status'))
    def get_status(self):
        return self.status

    @dbus.service.method(clipon_dbus_method('config'))
    def config(self, key, value):
        method = self.cfg.get_method(key)
        if method is None:
            logger.error("No method for key %s" % key)
            return False

        logger.info("Setting option %s to value %s" % (key, value))
        return method(value)

def main():
    daemon = CliponDaemon()
    daemon.start()
    print("Daemon started")

if __name__ == '__main__':
    main()
