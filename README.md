# kumo-manga
A web based manga reader.

### Dependencies

```
flask
flask_httpauth
rarfile
```

### Installation

Rename `default-config.json` to `config.json` and fill in the appropriate information.

Install the dependencies as listed above.

If you are one Windows, you will need to download `unrar.exe` and place it in the `deps` folder located at the root.

This has only been tested on Windows, but it should work on other systems.

### Usage

/list will be password protected by default (you can set whichever path to be required by auth).

Anything beyond list (ie, /list/Manga) will NOT be password protected (by default).