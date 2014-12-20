from distutils.core import setup
import py2exe
import requests.certs
build_exe_options = {"include_files":[(requests.certs.where(),'cacert.pem')]}
py2exe_options = {"bundle_files":1}

setup(
    name='PBWHelper',
    version='',
    packages=[''],
    url='https://github.com/BlackthornYugen/PBWHelper',
    license='',
    install_requires=[
      'requests',
      'rarfile',
      'py2exe'
    ],
    options={"py2exe": py2exe_options, "build_exe": build_exe_options},
    zipfile=None,
    data_files=[('',[requests.certs.where()])],
    console=['PyByWeb.py'],
    author='John Steel',
    author_email='',
    description=''
)
