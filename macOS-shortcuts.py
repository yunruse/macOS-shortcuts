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

# shortcut niceties

with open('codes.json') as f:
    CODES = json.load(f)

def to_vscode(string):
    for a, b in CODES.items():
        string = string.replace(a, b)
    return string

def from_vscode(string):
    for a, b in CODES.items():
        string = string.replace(b, a)
    return string

# plist handling

def plist_shortcuts(verbose=False, raw=False):
    PREFS = expanduser('~/Library/Preferences')

    shortcuts: dict[str, dict[str, str]] = {}
    for path in listdir(PREFS):
        if not path.endswith('.plist'):
            continue
        try:
            with open(join(PREFS, path), 'rb') as f:
                appShortcuts = plistlib.load(f).get('NSUserKeyEquivalents', None)
        except (plistlib.InvalidFileException, PermissionError) as e:
            if verbose:
                print('{}: {}'.format(path, e.args[-1]), file=stderr)
            continue
            
        if appShortcuts:
            appName = path.replace('.plist', '')
            shortcuts[appName] = {
                k: v if raw else to_vscode(v)
                for k, v in appShortcuts.items()}
    
    return shortcuts

# argument parsing

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument('--verbose', '-v', action="store_true",
    help="Output to stderr any info messages which are not errors.")
parser.add_argument('--raw', '-r', action="store_true",
    help="Output shortcuts as stored in .plist, rather than in an ASCII vscode format."
    " Note that some characters may be unprintable")

if __name__ == '__main__':
    # TODO: Import as well as export
    args = parser.parse_args()
    plists = plist_shortcuts(verbose=args.verbose, raw=args.raw)
    print(json.dumps(plists, indent=2))