# kumo-manga
A web based manga reader.

### Dependencies

```
flask
flask_httpauth
natsort
rarfile
```
#### Optional Dependencies
``
redis
```

## Installation

* Rename `default-config.json` to `config.json` and fill in the appropriate information.
* Install the dependencies as listed above.
* Setup and run redis, either including the below lines or appending it to the existing config in `/etc/redis.conf`.

#### redis.conf

```
maxmemory 500mb
maxmemory-policy allkeys-lru
maxmemory-samples 5
```

### Windows Setup

* You will need to download `unrar.exe` and place it in the `deps` folder located at the root.
* For redis, there is a Windows fork [here](https://github.com/rgl/redis/downloads).

## Usage

If you want a route to be password protected, add `@auth.login_required` below the last `@app.route()`.
