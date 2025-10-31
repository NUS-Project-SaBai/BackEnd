# Installing Python

For first timers, you may need to first install python, then a Python virtualenv management tool. Follow *The Hitchhiker's Guide to Python*:

## For Mac

- Follow the instructions at https://docs.python-guide.org/starting/install3/osx/#doing-it-right to install Homebrew and Python
- After installing Python via Homebrew, you should see an output like this: 
```
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
```
/opt/homebrew/opt/python@3.14/libexec/bin
```
- run `echo 'export PATH="<PATH-TO-BREW-PYTHON>:$PATH"' >> ~/.zshrc`, replacing `<PATH-TO-BREW-PYTHON>` with the one you see in the output above. This adds the path to the Homebrew-installed python to your PATH variable.
- then reload your shell:
```
source .zshrc
``` 
- now `python --version` should show something like: `Python 3.14.0`

## For Windows

https://docs.python-guide.org/starting/install3/win/#setuptools-pip

# Installing a Python virtualenvironment manager

[The guide](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) is slightly outdated for Python versions after 3.12, [as explained here](https://docs.brew.sh/Homebrew-and-Python?utm._source=chatgpt.com#pep-668-and-virtual-environments). Instead of `pip install --user pipenv`, do:
```
brew install pipx
pipx install pipenv
pipx ensurepath
source .zshrc
pipenv --verison
```
> `pipenv, version 2025.0.4`

Now that pipenv is available, you can use it to manage different Python versions for each project, enclosed in virtual environments. For Project Sabai, we will be using Python 3.12.