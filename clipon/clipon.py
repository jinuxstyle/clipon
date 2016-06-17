#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright (c) 2016, Jin Xu <jinuxstyle@hotmail.com>
#

from __future__ import absolute_import
from docopt import docopt
import sys
import client
from helper import INT_MAX
from defines import CLIPON_VERSION

__version__ = CLIPON_VERSION
__author__  = 'Jin Xu <jinuxstyle@hotmail.com>'

main_doc = """
A lightweight clipboard manager

Usage:
  clipon <command> [<options>...]

General Options:
  -h, --help    Show help
  --version     Show version and exit

Commands:
 start          Start clipon daemon
 list           List clipboard history
 clear          Clear history
 size           Total number of items
 config         Configure clipon
 info           Summary about clipon configuration and history
 pause          Pause tracking clipboard
 resume         Resume tracking clipboard
 stop           Stop and quit clipon daemon
 status         Status of clipon daemon

See 'clipon <command> -h' for more information on a specific command.
"""

list_doc = """
usage: clipon list [options]

List clipboard history tracked by clipon

Options:
  --number=<number> -n  Number of entries to be listed. Defaults to
                        total if not given
  --start=<start>       Starting entry number to list
  --reverse -r          List history entries in reverse order
  --short=<number>      Print at most given number of characters for each
                        entry to be listed. Defaults to all if not given
  --raw                 List history entries in raw format. Information
                        added by clipon are excluded.
  --before=<date time>  List history entries added before the given time

Examples:

  list all entries in raw and short format:
    $ clipon list --raw --short=80
  list the latest 10 entries:
    $ clipon list -n 10
  list the oldest 10 entries:
    $ clipon list -n 10 --start=0

"""

def do_list(args):
    num_entry   = args['--number']
    start_entry = args['--start']
    reverse     = args['--reverse']
    short       = args['--short']
    raw         = args['--raw']

    if num_entry is None:
        num_entry = INT_MAX
    else:
        num_entry = int(num_entry)
        if num_entry <= 0:
            print("Invalid value for option --number. Shall be greater than 0")
            return

    if start_entry is None:
        start_entry = -num_entry #from tail
    else:
        start_entry = int(start_entry)

    if short is None:
        short = INT_MAX
    else:
        short = int(short)
        if short <= 0:
            print("Invalid value for option --short. Shall be greater than 0")
            return

    client.print_history(start_entry, num_entry, raw, short, reverse)

delete_doc = """
usage: clipon delete [options]

Delete a number of entries in clip history

Options:
  --start=<number> -s   Starting from which one
  --number=<number> -n  Number of entries to be deleted [default: 1]

"""

def do_delete(args):
    start_entry = args['--start']
    num_entry = int(args['--number'])

    if num_entry <= 0:
        print("Invalid value for option --number. Shall be greater than 0")
        return

    if start_entry is None:
        print("Value not specified for option --start")
        return
    else:
        start_entry = int(start_entry)
        if start_entry < 0:
            print("Invalid value for option --start. Shall be greater or equal than 0")
            return

    client.delete_history(start_entry, num_entry)

config_doc = """
usage: clipon config [options]

Configure additional options

Options:
  --autosave=<string>       Save history to file automatically
  --max-entry=<number>      Maximum number of history entries, no limit
                            by default. Note that if there has already
                            more than the given number of entries, older
                            ones will be deleted.
  --max-length=<number>     Maximum number of characters for each entry,
                            no limit by default. Note that if the length
                            of a clip is longer than the given value, it
                            will be truncated to the given length. But it
                            doesn't apply to existing clips.

Examples:

  Do not save history to file
    $ clipon config --autosave false

"""

def do_config(args):
    autosave = args['--autosave']
    max_entry = args['--max-entry']
    max_length = args['--max-length']
    cfg = {}

    if autosave is not None:
        if autosave == 'False' or autosave == 'false':
            autosave = False
        elif autosave == 'True' or autosave == 'true':
            autosave = True
        else:
            print('Invalid value for option --autosave, shall be true or false')
            return
        cfg['autosave'] = autosave

    if max_entry is not None:
        max_entry = int(max_entry)
        if max_entry <= 0:
            print('Invalid value for --max_entry, shall be greater than zero')
            return
        cfg['max_entry'] = max_entry

    if max_length is not None:
        max_length = int(max_length)
        if max_length < 0:
            print('Invalid value for --max_length, shall be greater than zero')
            return

        cfg['max_length'] = max_length

    if len(cfg) > 0:
        client.config_clipon(cfg)

start_doc = """
usage: clipon start

Start clipon daemon
"""
def do_start(args):
    client.start_daemon()

stop_doc = """
usage: clipon stop

Stop clipon daemon
"""
def do_stop(args):
    client.stop_daemon()

pause_doc = """
usage: clipon pause

Pause clipon daemon
"""
def do_pause(args):
    client.pause_daemon()

resume_doc = """
usage: clipon resume

Pause clipon daemon
"""
def do_resume(args):
    client.resume_daemon()

size_doc = """
usage: clipon size

Get the total number of clips
"""
def do_size(args):
    size = client.get_size()
    print(size)

clear_doc = """
usage: clipon clear

Clear the clip history
"""
def do_clear(args):
    client.clear_history()

save_doc = """
usage: clipon save

Save clip history if autosave is not enabled
"""
def do_save(args):
    client.save_history()

def do_help(argv):
    if len(argv) == 0:
        docopt(main_doc, argv='-h')
    else:
        cmd = argv[0]
        cmd_doc = cmd + '_doc'
        try:
            print(globals()[cmd_doc])
        except KeyError:
            exit("%r is not a clipon command. See 'clipon -h|--help'." % cmd)

info_doc = """
usage: clipon info

Print summary info of clipon
"""
def do_info(args):
    client.print_info()

status_doc = """
usage: clipon status

Print status of clipon
"""
def do_status(args):
    client.print_status()

def main(argv=None):
    # parse the command line
    args = docopt(main_doc,
                  version='clipon version %s' % __version__,
                  options_first=True,
                  argv=argv or sys.argv[1:])
    cmd = args['<command>']
    argv = [args['<command>']] + args['<options>']

    if cmd == 'help':
        do_help(argv)
        return

    try:
        # parse the options for subcommand
        cmd_doc_name = cmd + '_doc'
        cmd_doc = globals()[cmd_doc_name]
        args = docopt(cmd_doc, argv)

        # call the subcommand handler
        method_name = 'do_' + cmd
        method = globals()[method_name]
        assert callable(method)
        method(args)
    except (KeyError, AssertionError):
        exit("%r is not a clipon command. See 'clipon help or clipon -h'." % cmd)

if __name__ == "__main__":
    main()
