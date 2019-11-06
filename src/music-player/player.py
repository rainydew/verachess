# coding: utf-8
# Copied from a coding forum and was modified
# Thank the origin author, although I cannot find the earliest person


class PlaysoundException(Exception):
    pass


def playsound(sound, block=True):
    """
    Utilizes windll.winmm. Tested and known to work with MP3 and WAVE on
    Windows 7 with Python 2.7. Probably works with more file formats.
    Probably works on Windows XP thru Windows 10. Probably works with all
    versions of Python.

    Inspired by (but not copied from) Michael Gundlach <gundlach@gmail.com>'s mp3play:
    https://github.com/michaelgundlach/mp3play

    I never would have tried using windll.winmm without seeing his code.
    """
    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if errorCode:
            errorBuffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
            try:
                exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                                                      '\n        ' + command.decode() +
                                    '\n    ' + errorBuffer.value.decode())
            except:
                exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                                                      '\n        ' + command.decode("gbk") +
                                    '\n    ' + errorBuffer.value.decode("gbk"))
            raise PlaysoundException(exceptionMessage)
        return buf.value

    alias = 'playsound_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

    if block:
        sleep(float(durationInMS) / 1000.0)
        winCommand('close', alias)


if __name__ == '__main__':
    import sys

    playsound(sys.argv[1])
