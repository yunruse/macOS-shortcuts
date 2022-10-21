'''
Tool for manipulating macOS keyboard shortcuts.

Finds all custom keyboard shortcuts and outputs a simple .json file.

No support for the opposite (ie "installing" a .json file) as of yet.
'''

from os import listdir
from os.path import join, expanduser
import plistlib
import json
from sys import stderr

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument('--verbose', '-v', action="store_true", help="Output to stderr any info messages which are not errors.")

class Shortcut(str):
    '''Some key combination as stored in .plist files'''
    # TODO: more user-friendly conversion -- function keys are private use Unicode for example
    #       try emulating vs-code style perhaps

AppShortcuts = dict[str, Shortcut]

def plist_shortcuts(verbose=False):
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
            if verbose:
                print('{}: {}'.format(path, e.args[-1]), file=stderr)
            continue
            
        if appShortcuts:
            appName = path.replace('.plist', '')
            shortcuts[appName] = {k: Shortcut(v) for k, v in appShortcuts.items()}
    
    return shortcuts

if __name__ == '__main__':
    # TODO: Import as well as export
    args = parser.parse_args()
    plists = plist_shortcuts(verbose=args.verbose)
    print(json.dumps(plists, indent=2))