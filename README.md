# Squirro Training Resources

Included here are a set of examples and training resources meant to accompany the [Squirro platform documentation](https://squirro.atlassian.net/wiki/display/DOC/Documentation) and [Squirro partner training resources](https://squirro.atlassian.net/wiki/display/TRAIN/Training)

## Getting Started

### Requirements
To use the examples here, you will need to install the squirro toolbox. The Squirro toolbox is available to all Squirro Partners and Developers [Here](https://squirro.atlassian.net/wiki/display/DOC/Toolbox)

### Python
To use the Squirro Toolbox, you must have Python2 intalled. Please note that the Squirro toolbox does not support Python3 (yet).

It is recommended to install python via [Homebrew](https://brew.sh/)
```bash
$ brew install python
```

### Virtualenvs
While not required, it is highly recommended that you create a virtual environment to use for squirro development.

To create a virtual environment, run the commands below (after you have Python installed)

```bash
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/.virtualenvs
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
```
Create the Virtualenv for Squirro
```bash
$ mkvirtualenv squirro
```
Once the virtualenv is created, you can switch into the new virtualenv by running:
```bash
$ workon squirro
```

If you want to automatically enter the virtualenv whenever you open a new terminal window, you can add the following to your bash profile:
```bash
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
# Set default virtualenv for python
workon squirro
```
