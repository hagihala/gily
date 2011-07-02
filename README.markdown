# What is this ?

This script is clone of [git-wiki](https://github.com/sr/git-wiki) written by Python and Flask.

# Requirements

* Flask
* Git-Python

# How to use

1. `git clone git://github.com/nyarla/gily.git && cd gily`
2. `emacs -nw config.py`
3. `./server.py --debug` or push [dotcloud](http://www.dotcloud.com/)

*config.py example*

    # -*- encoding: utf-8 -*-

    REPOSITORY     = './data'
    FILE_EXTENSION = 'txt'
    HOMEPAGE       = 'ReadMe'

# Author

Naoki Okamura (Nyarla) *nyarla[ at ]thotep.net* (Japanese)

# License

this script is under public domain.