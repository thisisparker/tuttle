TUTTLE DEV ENVIRONMENT
======================

Pre-requisites
--------------

Follow the `signal-cli` documentation to install and configure that program with a new number.

Ensure `tor` is installed, and modify the `torrc` file to serve localhost:5000 as a hidden service. Restart `tor` and record the hostname it generates.

Tuttle installation
-------------------

Git clone the tuttle directory.

Install python requirements. May be as simple as:

```
pip install -r requirements.txt
```

but may require some system dependencies:

```
sudo apt install python3-gi
```

Modify the two configuration files, `config.yaml.sample` and `settings.py.sample`, saving each without the `.sample` suffix. The number provided in the `config` file should be your primary Signal number, on which you intend to receive notifications. The number in the `settings` file should be the new number with which you've configured `signal-cli`.

In separate terminal sessions, run

```
flask run
```
and
```
./logincoming.py
```

Each is fairly verbose, and will provide lots of running feedback on how the process is running.
