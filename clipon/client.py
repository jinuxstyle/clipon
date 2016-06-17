#!/usr/bin/env python3
from __future__ import absolute_import
import dbus
import json
import subprocess
from time import sleep
from defines import *
import sys
import os

"""
Client module for communicating with daemon via DBus
"""

def clipon_dbus_req(name):
    req = None

    bus = dbus.SessionBus()
    try:
        bus.get_name_owner(CLIPON_BUS_NAME)
    except dbus.DBusException as e:
        start_daemon()

    try:
        session = bus.get_object(CLIPON_BUS_NAME, CLIPON_OBJ_PATH)
        method = CLIPON_BUS_NAME + '.' + name
        req = dbus.Interface(session, method)
    except dbus.DBusException as e:
        print("Could not connect to daemon, make sure daemon has been started\n" + str(e))

    return req

def print_status():
    req = clipon_dbus_req('get_status')
    if req is None:
        return

    print(req.get_status())

def config_clipon(cfg):
    req = clipon_dbus_req('config')
    if req is None:
        return

    for key, value in cfg.items():
        ret = req.config(key, value)
        if not ret:
            print("Failed to set option %s to value %s" % (key, value))

def print_info():
    req = clipon_dbus_req('get_info')
    if req is None:
        return

    info = req.get_info()
    if info is not None:
        info = json.loads(info) #convert to dict
        print(json.dumps(info, sort_keys=True, indent=5, separators=(',', ': ')))

def clear_history():
    req = clipon_dbus_req('clear_history')
    if req is None:
        return

    req.clear_history()

def get_size():
    req = clipon_dbus_req('history_size')
    if req is None:
        return

    size = req.history_size()
    return int(size)

def pause_daemon():
    req = clipon_dbus_req('pause')
    if req is None:
        return
    req.pause()

def resume_daemon():
    req = clipon_dbus_req('resume')
    if req is None:
        return
    req.resume()

def save_history():
    req = clipon_dbus_req('save_history')
    if req is None:
        return

    req.save_history()

def ping_daemon():
    bus = dbus.SessionBus()
    try:
        session = bus.get_object(CLIPON_BUS_NAME, CLIPON_OBJ_PATH)
    except Exception:
        return False
    return True

def start_daemon():
    cwd = os.path.dirname(os.path.abspath(__file__))
    daemon_path = os.path.join(cwd, 'daemon.py')
    fd = open('/dev/null', 'a+')
    subprocess.Popen(['python', daemon_path], stdin=fd, stdout=fd, stderr=fd)
    ready = ping_daemon()
    while not ready:
        sleep(0.1) #sleep 1 millisecond
        ready = ping_daemon()

    if ready:
        print("Daemon started")

def stop_daemon():
    req = clipon_dbus_req('stop')
    if req is None:
        return
    req.stop()
    print("Daemon stopped")

def print_history(start, number, raw, short, reverse):
    req = clipon_dbus_req('history_size')
    if req is None:
        return
    size = req.history_size()
    if size == 0:
        print("History is empty")
        return

    if number > size:
        number = size

    if start < 0:
        start = size + start #starting from the tail
        if start < 0:
            start = 0

    end = start + number

    if end > size:
        end = size

    if start >= end:
        print("Invalid range [%d, %d). Total is %d\n" % (start, end, size))
        return

    if reverse:
        num_range = reversed(range(start, end))
    else:
        num_range = range(start, end)

    req = clipon_dbus_req('get_clip_entry')
    if req is None:
        return

    for index in num_range:
        # Call the methods using the interface
        entry = req.get_clip_entry(index)
        if entry is None:
            print("Entry %s not exists" % index)
            continue

        entry = json.loads(entry)
        text = entry.get('text', None)

        if entry is None:
            print("Invalid entry %s" % index)
            continue

        if short < len(text):
            text = text[0:short]

        if raw:
            print("%s" % text)
        else:
            print("%d: %s" % (index, text))

def delete_history(start, number):
    req = clipon_dbus_req('del_history')
    if req is None:
        return
    req.del_history(start, start + number)
