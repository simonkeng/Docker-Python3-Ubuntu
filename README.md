# Dockerized Ubuntu 18.04 with Python 3.7.3, built from source

Massive credit & thanks to [@matthewfeickert](https://github.com/matthewfeickert) who wrote the shell script to compile Python, as well as everything else in this repo. [Ubuntu 18.04](https://wiki.ubuntu.com/BionicBeaver/ReleaseNotes/18.04) comes with support for many powerful data science utilities and machine learning libraries, with [Python 3.7](https://www.python.org/downloads/release/python-372/) compiled and ready to go, this is a great sandbox for development and testing data science tools that require Ubuntu 18/Python 3.7. 

# Instructions

1. Clone this repo: `git clone https://github.com/simonkeng/ubuntu18python37.git`

2. Run the `Makefile` to automate the docker build commands. The image will be built as `ubuntu18python37`. 

```bash
$ ls
Dockerfile        LICENSE           Makefile          README.md         install_python.sh
$ make
```

## Installed Dependencies

### apt-get
- gcc
- g++
- git
- zlibc
- zlib1g-dev
- libssl-dev
- libbz2-dev
- libsqlite3-dev
- libncurses5-dev
- libgdbm-dev
- libgdbm-compat-dev
- liblzma-dev
- libreadline-dev
- uuid-dev
- libffi-dev
- tk-dev
- wget
- curl
- make
- software-properties-common

### From source

- Python 3.7 (3.6)

