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

If you want a route to be password protected, add `@auth.login_required` below the last `@app.route()`.