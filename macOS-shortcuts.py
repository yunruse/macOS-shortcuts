'''
Tool for manipulating macOS keyboard shortcuts.

Currently only does basic output.
'''

from os import listdir
from os.path import join, expanduser
import plistlib
import json
from sys import stderr


class Shortcut(str):
    '''
    Some key combination that would be stored in a .plist.
    '''
    # TODO: fancy display & conversion -- function keys don't look nice

AppShortcuts = dict[Shortcut, str]

class AppName(str):
    '''
    Some application name, e.g. com.apple.Music
    '''
    # TODO: is it possible to convert?


def plist_shortcuts():
    PREFS = expanduser('~/Library/Preferences')

    shortcuts: dict[str, AppShortcuts] = {}
    for path in listdir(PREFS):
        if not path.endswith('.plist'):
            continue
        appShortcuts: dict[str, str]
        try:
            with open(join(PREFS, path), 'rb') as f:
                appShortcuts = plistlib.load(f).get('NSUserKeyEquivalents', None)
        except (plistlib.InvalidFileException, PermissionError) as e:
            print('{}: {}'.format(path, e.args[-1]), file=stderr)
            continue
            
        if appShortcuts is not None:
            appName = AppName(path.replace('.plist', ''))
            shortcuts[appName] = {Shortcut(v): k for k, v in appShortcuts.items()}
    
    return shortcuts

if __name__ == '__main__':
    plists = plist_shortcuts()
    print(json.dumps(plists, indent=2))