# Clipon - A Lightweight Clipboard Manager

Clipon is a open source project for managing your clipboard history
in a simple and efficient way.

It's useful when you want to take notes from some interesting documents
or web pages you are reading. But you might not want to do copy and paste
frequently. Because the paste operation needs you switch to another app
to do paste and then switch back, which is kind of a distraction. with
Clipon, you just copy things when reading, and do paste in batch after
reading.

It also helps remember what you have copied and you might later want to
revisit some of them.

## Installation

Install required packages first

1. [PyGI](https://wiki.gnome.org/PyGObject)

    It is not packaged in pypi, so you have to install it by youself.
    Depending on your distribution, the package are usually named python-gi,
    python-gobject or pygobject3.

2. python-dbus

    You can install it from pypi using pip tool or using package
    management tool of your distribution.

3. docopt

    It can be installed automatically when installing the Clipon (see
    below). So it's not necessary to install it by youself.

Then install Clipon


    $ git clone https://github.com/jinuxstyle/clipon.git
    $ cd clipon
    $ python setup.py install

## Usage

After installation, start the daemon

    $ clipon start

Then you can view the clipboard history with following command

    $ clipon list

Clipon supports a number of subcommands for controlling the daemon and
managing the clipboard history.

    $ clipon -h | --help
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

## Development

You can contribute and help in various ways including reporting bugs,
proposing suggestions or ideas, and submitting pull requests.

## License

Clipon is under the GPL license.
