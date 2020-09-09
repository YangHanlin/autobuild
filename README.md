# Autobuild: A simple cross-platform build script for C++

[![Issues](https://img.shields.io/github/issues/YangHanlin/autobuild?style=flat-square)](https://github.com/YangHanlin/autobuild/issues) [![Pull requests](https://img.shields.io/github/issues-pr/YangHanlin/autobuild?style=flat-square)](https://github.com/YangHanlin/autobuild/pulls) [![License](https://img.shields.io/github/license/YangHanlin/autobuild?style=flat-square)](LICENSE)

**Autobuild** is a simple Python script to build a simple C++ program based on one file or all files in the same directory, which aims to fit the interfaces of editors, such as Visual Studio Code.

## Dependencies

- Python 3
- A C++ Compiler (G++ or some compiler compatible)
- Make

## Installation & Configuration

### Installation

#### Windows with Scoop

It is recommended on Windows to install Autobuild with [Scoop](https://scoop.sh/).

1. Add the bucket [Orihime 1](https://github.com/YangHanlin/OrihimeFirst) to Scoop (if you have never done so):

   ```powershell
   scoop bucket add orihime https://github.com/YangHanlin/OrihimeFirst
   ```

2. Install Autobuild with one command:

   ```powershell
   scoop install orihime/autobuild-insider  # stable version not available yet
   ```

3. Run command `autobuild` (instead of `autobuild.py`, because Scoop actually creates a shim named `autobuild`) to check, which, if configured correctly, will result in the following output:

   ```powershell
   usage: autobuild.py [-h] -t TARGET [-d DIR] [-c FLAGS] [-m FLAGS] [-V] SOURCE
   autobuild.py: error: the following arguments are required: SOURCE, -t/--target
   ```

#### Not Windows, or without Scoop

If you do not have Scoop installed or you are not working on Windows, you can also perform installation steps manually.

1. Clone (which is recommended because it enables you to stay updated) or download the repository;

2. Add path of the directory containing downloaded files into the `PATH` environment variable;

3. Run command `autobuild.py` to check, which, if configured correctly, will result in the following output:

   ```
   usage: autobuild.py [-h] -t TARGET [-d DIR] [-c FLAGS] [-m FLAGS] [-V] SOURCE
   autobuild.py: error: the following arguments are required: SOURCE, -t/--target
   ```

### Configuration

Find the configuration file `.autobuildrc` in your user home directory (`%USERPROFILE%` on Windows or `$HOME` on \*nix), open and edit it:

   - Check whether the value of `cc`, which indicates the command to invoke the compiler, by default `g++`, works as a compiler and as desired. If your desired compiler is not compatible with `g++`, modify `cc-flags` as well to fit your compiler’s interface.

   - Check whether the value of `make`, which indicated the command to invoke Make and is by default `make`, works as desired. You may add `make-flags` to define the flags passed to Make by default.

## Usage

```
$ autobuild.py --help
usage: autobuild.py [-h] -t TARGET [-d DIR] [-c FLAGS] [-m FLAGS] [-V] SOURCE

A simple cross-platform build script for C++.

positional arguments:
  SOURCE                filename or path of (one of) the source file(s)

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        filename or path of the built target
  -d DIR, --change-dir DIR
                        change the working directory to the specified one
                        before building
  -c FLAGS, --cc-flags FLAGS
                        additional flags passed to the compiler
  -m FLAGS, --make-flags FLAGS
                        additional flags passed to Make
  -V, --version         show version information and exit
```

## License

All content in this repository, unless otherwise noted, is licensed under [the GNU General Public License 3.0 (GPLv3)](LICENSE).
