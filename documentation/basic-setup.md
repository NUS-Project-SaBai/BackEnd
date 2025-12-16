# Installing Python

For first timers, you may need to first install python, then a Python virtualenv management tool. This setup guide will follow *The Hitchhiker's Guide to Python*:

## For Mac

- Follow the instructions at https://docs.python-guide.org/starting/install3/osx/#doing-it-right to install Homebrew and Python
- After installing Python via Homebrew, you should see an output like this: 
```bash
==> Summary
🍺  /opt/homebrew/Cellar/python@3.14/3.14.0_1: 3,759 files, 69.6MB
==> Running `brew cleanup python@3.14`...
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Caveats
==> python@3.14
Python is installed as
/opt/homebrew/bin/python3

Unversioned symlinks `python`, `python-config`, `pip` etc. pointing to
`python3`, `python3-config`, `pip3` etc., respectively, are installed into
/opt/homebrew/opt/python@3.14/libexec/bin

`idle3.14` requires tkinter, which is available separately:
brew install python-tk@3.14

See: https://docs.brew.sh/Homebrew-and-Python
```
- look for the path to the installed python, in this case it is:
```bash
/opt/homebrew/opt/python@3.14/libexec/bin
```
- run `echo 'export PATH="<PATH-TO-BREW-PYTHON>:$PATH"' >> ~/.bashrc`, replacing `<PATH-TO-BREW-PYTHON>` with the one you see in the output above. This adds the path to the Homebrew-installed python to your PATH variable.
- then reload your shell:
```bash
source .bashrc
``` 
- now `python --version` should show something like: `Python 3.14.0`

## For Windows

https://docs.python-guide.org/starting/install3/win/#setuptools-pip

# Installing a Python virtual environment manager

We will be using [Pipenv](https://pipenv.pypa.io/en/latest/), which is well established and easy to use, serving as both a package manager and a virtual environment manager.

The [guide for installing Pipenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) on *The Hitchhiker's Guide to Python* is slightly outdated for Python versions after 3.12, [as explained here](https://docs.brew.sh/Homebrew-and-Python?utm._source=chatgpt.com#pep-668-and-virtual-environments). Instead of `pip install --user pipenv`, install [pipx](https://github.com/pypa/pipx) and use that instead:

```bash
brew install pipx
pipx install pipenv
pipx ensurepath
source .zshrc 
```
(or `.bashrc`, depending on what you're using)
Now verify the installation:
```
pipenv --verison
```

(The latest Pipenv version at the time of writing is `version 2025.0.4`)

Now that pipenv is available, you can use it to manage different Python packages for each project, enclosed in a virtual environment. 

# Installling a Python version manager

Next you need a Python version manager. Pipenv works with [pyenv](https://github.com/pyenv/pyenv), so we'll get that:

```bash
brew install pyenv
```

# Setting up the environment
For Project Sabai, we will be using Python 3.12. Simply attempt to create a pipenv virtualenv in your project directory, and it will prompt you to install Python 3.12 with pyenv:

```bash
pipenv --python 3.12
```

Accept the prompts, and you should be good to go.

To use the virtual environment, run:

```bash
pipenv shell
```

To exit from the virtual environment, run: (don't exit if you intend to continue with the setup in [README.md](../README.md))

```bash
exit
```
