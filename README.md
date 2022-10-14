# Python Packaging Example
This tutorial and example is based on [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

## Generating distribution archives
The next step is to generate distribution packages for the package. These are archives that are uploaded to the Python Package Index and can be installed by pip.

Make sure you have the latest version of PyPA’s build installed:
```
python3 -m pip install --upgrade build
```

Now run this command from the same directory where [pyproject.toml](./pyproject.toml) is located:

```sh
python3 -m build
```
This command should output a lot of text and once completed should generate two files in the dist directory:
```log
dist/
├── example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
└── example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
```
The `tar.gz` file is a source distribution whereas the `.whl` file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source distributions if needed. You should always upload a source distribution and provide built distributions for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.

## Uploading the distribution archives
Finally, it’s time to upload your package to the Python Package Index!

The first thing you’ll need to do is register an account on TestPyPI, which is a separate instance of the package index intended for testing and experimentation. It’s great for things like this tutorial where we don’t necessarily want to upload to the real index. To register an account, go to https://test.pypi.org/account/register/ and complete the steps on that page. You will also need to verify your email address before you’re able to upload any packages. For more details, see Using TestPyPI.

To securely upload your project, you’ll need a PyPI API token. Create one at https://test.pypi.org/manage/account/#api-tokens, setting the “Scope” to “Entire account”. **Don’t close the page until you have copied and saved the token — you won’t see that token again.**

Now that you are registered, you can use *twine* to upload the distribution packages. You’ll need to install Twine:

```sh
python3 -m pip install --upgrade twine
```

Once installed, run Twine to upload all of the archives under `dist`:

```sh
python3 -m twine upload --repository testpypi dist/*
```
You will be prompted for a username and password. For the username, use __token__. For the password, use the token value, including the pypi- prefix.

After the command completes, you should see output similar to this:
```log
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: __token__
Uploading example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.2/8.2 kB • 00:01 • ?
Uploading example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.8/6.8 kB • 00:00 • ?
```
Once uploaded, your package should be viewable on TestPyPI; for example: `https://test.pypi.org/project/example_package_YOUR_USERNAME_HERE`.

## Installing your newly uploaded package
You can use pip to install your package and verify that it works. Create a virtual environment and install your package from TestPyPI:
```sh
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-rrmhearts
```

Make sure to specify your username in the package name!

pip should install the package from TestPyPI and the output should look something like this:
```log
Collecting example-package-YOUR-USERNAME-HERE
  Downloading https://test-files.pythonhosted.org/packages/.../example_package_YOUR_USERNAME_HERE_0.0.1-py3-none-any.whl
Installing collected packages: example_package_YOUR_USERNAME_HERE
Successfully installed example_package_YOUR_USERNAME_HERE-0.0.1
```
Note This example uses `--index-url` flag to specify TestPyPI instead of live PyPI. Additionally, it specifies `--no-deps`. Since TestPyPI doesn’t have the same packages as the live PyPI, it’s possible that attempting to install dependencies may fail or install something unexpected. While our example package doesn’t have any dependencies, it’s a good practice to avoid installing dependencies when using TestPyPI.
You can test that it was installed correctly by importing the package. Make sure you’re still in your virtual environment, then run `python3` and import the package:
```py
>>> from example_package_YOUR_USERNAME_HERE import example
>>> example.add_one(2)
3
```

## Setup.py
The smallest python project is two files. A setup.py file which describes the metadata about your project, and a file containing Python code to implement the functionality of your project. **While `setup.py` is now considered replaced by `pyproject.toml` it is still relevant and heavily used**.

The setup.py file is at the heart of a Python project. It describes all of the metadata about your project. There a quite a few fields you can add to a project to give it a rich set of metadata describing the project. However, there are only three required fields: name, version, and packages. The name field must be unique if you wish to publish your package on the Python Package Index (PyPI). The version field keeps track of different releases of the project. The packages field describes where you’ve put the Python source code within your project.

Our initial setup.py will also include information about the license and will re-use the README.txt file for the long_description field. This will look like:
```py
from distutils.core import setup

setup(
    name='TowelStuff',
    version='0.1dev',
    packages=['towelstuff',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
```
To create a release using `setup.py`, your source code needs to be packaged into a single archive file. This can be done with the sdist command:
```sh
python setup.py sdist
```
This will create a dist sub-directory in your project (*an egg*), and will wrap-up all of your project’s source code files into a distribution file, a compressed archive file in the form of: `TowelStuff-0.1.tar.gz`

You can register your package with pypi and upload your release with the following:
```
# Choose project name: http://pypi.python.org/pypi/<projectname>

python setup.py register
python setup.py sdist bdist_wininst upload
```
## Next steps
Keep in mind that this tutorial showed you how to upload your package to Test PyPI, which isn’t a permanent storage. The Test system occasionally deletes packages and accounts. It is best to use TestPyPI for testing and experiments like this tutorial.

When you are ready to upload a real package to the Python Package Index you can do much the same as you did in this tutorial, but with these important differences:

Choose a memorable and unique name for your package. You don’t have to append your username as you did in the tutorial, but you can’t use an existing name.

Register an account on https://pypi.org - note that these are two separate servers and the login details from the test server are not shared with the main server.

Use twine upload `dist/*` to upload your package and enter your credentials for the account you registered on the real PyPI. Now that you’re uploading the package in production, you don’t need to specify --repository; the package will upload to https://pypi.org/ by default.

Install your package from the real PyPI using `python3 -m pip install [your-package]`.

At this point if you want to read more on packaging Python libraries here are some things you can do:

Consider packaging tools that provide a single command-line interface for project management and packaging, such as hatch, flit, pdm, and poetry.

Read PEP 517 and PEP 518 for background and details on build tool configuration.

Read about Packaging binary extensions.