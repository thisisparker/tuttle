On a server where `signal-cli` has already been configured, `logincoming.py` can be run as a background process to receive and log incoming Signal messages. `app.py` can be run with `flask` to serve on a localhost port a dynamic admin interface generated by `readlog.py`, and an externally configured Onion service can make that interface more generally available.

This is a work in progress and should not be used in production.
