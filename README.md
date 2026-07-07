# PythonStarterPack python package

main sources used for the building process

- [Packaging Python](https://packaging.python.org/en/latest/overview/)
- [Setuptools](https://setuptools.pypa.io/en/latest/userguide/index.html)

## changelog

- v0.0.1 : First Release
- v0.0.2 :
    - console intgration improvement, using rich console features
    - global QOL and typo corrections
    - Readme edit

## install PythonStarterPack

retrieve the installation package in the release

then install it with pip :

`pip install pythonstarterpack-0.0.2-py3-none-any.whl`

or

`pip install pythonstarterpack-0.0.2.tar.gz`

## setup project

install the package PythonStarterPack

then execute the following command :

`python -m PySP`

or

`PySP-new`

you will be guided through the project creation


## setup env

If you installed a venv a the project creation (which is recommanded), you will have a folder named `pyenv` (or whatever you chose) containing it.
You will then want to activate it with the following command :

windows :
`<venv>/Scripts/activate`

linux (bash):
`source <venv>/bin/activate`


type `deactivate` to disable the venv

[venv doc](https://docs.python.org/3/library/venv.html)

---

once activated check the pachage installed with `pip list`


before starting to work on your code, you will have to install your project in your env in developement mode (that is to facilitate the packaging of your project)

`pip install --editable .`

> this should be already installed after creation with the tool, but you will need to rerun the command if you make structure modifications or changes in the pyproject.toml

if you have a proxy :

`pip install --editable . --proxy http://user:pass@10.10.10.10:1111`

## execute your code

in your env you can invoke your code with two methods :

`python -m [project_name]`

## build your package

to be able to distribute your package you will want to build it, fortunately if your followed the full project creation you already have the necessary tools installed

- setuptools
- build

then to build your project, just run `python -m build --no-isolation`

a dist folder will be created at the root of your project containing the installable files for your package

you will want to configure the metadata of your project in the `pyproject.toml` file, more information at [setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
