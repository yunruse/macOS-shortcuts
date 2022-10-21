# macos-Shortcuts.py

Basic tool for managing macOS' custom keyboard shortcuts.

See https://apple.stackexchange.com/a/449161/475818 for an explanation.

## Usage

With no input, outputs the current shortcuts to stdout in JSON format. For example:

```bash
$ python macOS-shortcuts.py
{
  "com.apple.Safari": {
    "Pin Tab": "command+p",
    "Unpin Tab": "command+p"
  },
  ".GlobalPreferences": {
    "System Settings\u2026": "control+,",
  },
  "com.apple.finder": {
    "Rename": "command+r"
  }
}
```