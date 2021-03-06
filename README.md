Learning Registry Installation and Configuration
================================================

License & Copyright
===================

Copyright 2011 SRI International

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Overview of Contents
====================

* config
    * setup_node.py - simple script to configure a couch instance for an lr use.

* couchdb/apps
    * stemx - NSDL STEM Exchange Demo couch application
* couchdb/tests
    * stemx - scripts for testing STEM Exchange couch app
    * generate-json-evelope-data.py - OBSOLETE

* data-pumps
    * del-contents.py - simple script to delete contents of a couchdb minus design documents.
    * nsdl-to-lr-data-pump.py - OAI-PMH harvester; data pump script from NDSL-DC -> LR RDDDM
    * sample-pump-oaipmh-lib.py - OBSOLETE; here for reference.

* install
    * setup_lr.bash - a script to set up a development Learning
      Registry node on Ubuntu 10.04 and MacOS 10.6.x onwards.
    * install_pydeps.bash - a script to create a virtualenv and
      install the Learning Registry Pylons application in that
      virtualenv.

* LR - Pylons LR application that is used to interface w/ CouchDB.

* search - ??? A simple search UI to be installed in a design document.  _TODO: move into a couchapp._


Installation on Turnkey Core (Ubuntu 10.04 LTS)
===============================================

## Configure apt sources ##

* Edit the sources list

>       sudo vim /etc/apt/source.list.d/sources.list

* Add deb restrticted and multiverse, plus add deb-src for all:

>       deb http://us.archive.ubuntu.com/ubuntu lucid main universe restricted multiverse
>       deb http://us.archive.ubuntu.com/ubuntu lucid-updates main universe restricted multiverse
>       deb-src http://us.archive.ubuntu.com/ubuntu lucid main universe restricted multiverse
>       deb-src http://us.archive.ubuntu.com/ubuntu lucid-updates main universe restricted multiverse

* Update apt sources

>       sudo apt-get update


## Install curl ##

* Use apt-get to install curl

>       sudo apt-get install libcurl3 curl


## Install Python setup tools ##

* Install Python easy_setup

>       sudo apt-get install python-pkg-resources python-setuptools


## Install CouchDB ##

* Build CouchDB dependencies

>       sudo apt-get build-dep couchdb

* Install other dependencies

>       sudo apt-get install xulrunner-dev libicu-dev libcurl4-gnutls-dev libtool

* Then create /etc/ld.so.conf.d/xulrunner.conf.

>   a. To check what XULRunner version you have installed:

>       xulrunner -v

>   b. Configure xulrunner

>   >   i. Edit the xulrunner.conf

>   >       sudo vi /etc/ld.so.conf.d/xulrunner.conf

>   >   ii. Add the following edits, replacing the x.x.x.x with your version number.

>   >       /usr/lib/xulrunner-x.x.x.x
>   >       /usr/lib/xulrunner-devel-x.x.x.x

>   c. Update ldconfig

>       sudo /sbin/ldconfig

* Download CouchDB from http://couchdb.apache.org/downloads.html.

* Untar (decompress) the source file:

>       tar -zxvf apache-couchdb-x.x.x.tar.gz

* Change into the expanded directory:

>       cd apache-couchdb-x.x.x

* Install SpiderMonkey (see below)

* Configure the build:

>       LDFLAGS="$(pkg-config mozilla-js --libs-only-L)" CFLAGS="$(pkg-config mozilla-js --cflags)" ./configure

* Build CouchDB:

>       make

* Fix any errors

* Install CouchDB to default location:

>       sudo make install

* Add couchdb user account

* change file ownership from root to couchdb user and adjust permissions

>       sudo chown -R couchdb: /usr/local/var/{lib,log,run}/couchdb /usr/local/etc/couchdb
>       sudo chmod 0770 /usr/local/var/{lib,log,run}/couchdb/
>       sudo chmod 664 /usr/local/etc/couchdb/*.ini
>       sudo chmod 775 /usr/local/etc/couchdb/*.d

* install init script and start couchdb

>       cd /etc/init.d
>       sudo ln -s /usr/local/etc/init.d/couchdb couchdb
>       sudo /etc/init.d/couchdb start

* configure couchdb to start on system start

>       sudo update-rc.d couchdb defaults

* Verify couchdb is running

>       curl http://127.0.0.1:5984/

* To accesses futon remotely and run tests, update the bind address in local.ini:

>       sudo vim /usr/local/etc/couchdb/local.ini
>            [httpd]
>            ; Bind to all addresses
>            bind_address = 0.0.0.0

* Restart couchdb

>       sudo service couchdb restart


## Install SpiderMonkey ##

* Get one of the source tarballs from http://ftp.mozilla.org/pub/mozilla.org/js/ (1.7.0 or 1.8.0-rc1 will do).

* Unpack the tarball. Note that once extracted the source are in the directory "js", without the expected version suffix.

* Go to the js/src directory.

>       cd js/src

* Build SpiderMonkey. There is no default Makefile, use Makefile.ref. The default build is debug, use BUILD_OPT=1 for an optimized build.

>       make BUILD_OPT=1 -f Makefile.ref

* Install SpiderMonkey. Instead of "install" the target to use is "export". Instead of PREFIX the target directory is specified with JS_DIST.

>       sudo make BUILD_OPT=1 JS_DIST=/usr/local -f Makefile.ref export

## Configure logrotate to rotate and compress CouchDB log files

* These steps are only necessary if you installed from source.

* Open logrotate.conf.

* Uncomment the the compress option, this will allow logrotate to compress old log files into a gzip file.

* run ln -s /usr/local/etc/logrotate.d/couch /etc/logrotate.d/couchdb as root or using sudo to create the couchdb entry for logrotate


## Install Yajl 1.0.12 ##

* Install Yajl dependencies

>       sudo apt-get install ruby cmake

* Download and extract and build Yajl 1.0.12 from here http://lloyd.github.com/yajl/

>       sudo make
>       sudo make install

* Update your LD_LIBRARY_PATH to include /usr/local/lib. Add the following line to ~learningregisty/.bashrc.d/defaults or /etc/bach.bashrc

>       export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH


## Install Python virtualenv and Pylons ##

* Install virtualenv

>       sudo easy_install virtualenv

* Install required library dependencies

>       sudo apt-get install python-dev python-libxml2 python-libxslt1 libxml2-dev libxslt1-dev

* Create a user for learningregistry and su to user

>       su learningregistry

* Create a directory for the virtualenv

>       mkdir virtualenv
>       cd virtualenv

* Create virtualenv for LR

>       virtualenv --distribute lr
>       cd lr/bin/

* Install LR Python deps

>       ./pip install pylons
>       ./pip install flup
>       ./pip install pyparsing
>       ./pip install --upgrade couchdb
>       ./pip install restkit
>       ./pip install cython
>       ./pip install lxml
>       ./pip install iso8601plus
>       ./pip install ijson


## Configure Nginx - Should be preinstalled on Ubuntu ##

* Backup your original nginx.conf file

>       sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak

* Copy the ngnix.conf file from repository

>       sudo cp nginx.conf /etc/nginx/nginx.conf
## Configure Pylons logging level

* Edit the production.ini found at LearningRegistry/LR

* Modify the level value under the logger_lr section

* For production is is set to only log error messages, for more verbose logging it can be set to info

## Start LR code ##

* From your virtualenv directory start paster where */home/learningregistry/virtualenv/lr* is my path to virtualenv.
>       /home/learningregistry/virtualenv/lr/bin/paster serve --daemon production.ini start


Automated Installation on Ubuntu 10.04 onwards and MacOS 10.6.x (Snow Leopard)
===========================================

These instructions make use of a provided installation script to
install nearly all the software required to run a development Learning
Registry node on Ubuntu 10.04 and MacOS 10.6.x onwards. A node set up
using this script has not been tested in production. If you are
feeling intrepid, do share your experiences on the mailing list.

The installation script downloads and installs the
[CouchBase Server Community Edition](http://www.couchbase.com/downloads)
http://www.couchbase.com/downloads on Ubuntu since compilation is
fiddly and this package works beautifully.

## Ubuntu Requirements ##
* Git, which is not available on 10.04 by default, but is available on
  newer versions. If you want to have the latest stable version
  installed you can use the Git stable releases PPA at
  https://launchpad.net/~git-core/+archive/ppa

## MacOS Requirements ##
* Xcode developer tools. Downloadable from the Apple Developer site at
  http://developer.apple.com. Currently Xcode 3 works better than
  Xcode 4.
* [Homebrew](https://github.com/mxcl/homebrew) package manager. The
  brew command should be in your path.
* Git, which you very likely already have if you have installed
  Homebrew. But can be installed from Homebrew.

**Note:** There is an issue installing lxml with Xcode 4, which is not
  required to run the Pylons app, but is required to run the tests. If
  Xcode 4 is installed, the script will not install lxml. See
  https://gist.github.com/963298 for instructions on manually
  installing lxml with Xcode 4.

## Installation ##
* Clone this repository. If you are viewing this page on github, you
  should see the clone URL near the top of the page.

* Change directory to install directory in the cloned Learning
  Registry git repository.

>       cd <path to clone of the git repository>/install

* Run the setup_lr.bash script. You may optionally supply the name of
  the virtualenv in which the python packages will be installed as an
  argument to the install script. If no argument is supplied, it will
  create a virtualenv named *lr* in your home directory or in the
  virtualenvwrapper workspace if
  [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)
  is installed and configured.

>       bash ./setup_lr.bash [optional name of virtualenv]

## Setup ##
* Activate the virtualenv the script created. It should have printed
  out instructions on how to do so.

* Start up couchdb. On Ubuntu, the CouchBase server is started up
  automatically after installation by the CouchBase package. You need
  *only* do the step below on MacOS.

>       launchctl load -w /usr/local/Cellar/couchdb/1.0.2/Library/LaunchDaemons/org.apache.couchdb.plist

* Create a development configuration file. You may copy the original
  configuration file in the LR directory.

>       cp LR/development.ini.orig LR/development.ini

* Navigate to the `config` directory within your clone of the Learning
  Registry git repository.

>       cd config

* Load the initial documents for Learning Registry into CouchDB. This
  script will ask a few questions.

>       ./setup_node.py

* Edit the development.ini file and replace the line
  `use = egg:Flup#fcgi_thread` with `use = egg:Paste#http`.

## Start up the node ##
* Run the development web server.

>       paster serve --reload development.ini

* Check to see if all is well by checking the status of the node we
  have just set up. You should receive a response if it's working.

>       curl -i http://127.0.0.1:5000/status


Manual Installation on MacOS 10.6.x (Snow Leopard)
===========================================

These instructions are provided for use by developers who may be
interested in running LR on MacOS 10.6.x for development
purposes. MacOS has not been tested for deployment of a production
Learning Registry node.

## Requirements ##
* Xcode developer tools. Downloadable from the Apple Developer site at
  http://developer.apple.com.
* [Homebrew](https://github.com/mxcl/homebrew) package manager. The
  brew command should be in your path.
* Git, which you very likely already have if you have installed
  Homebrew. But can be installed from Homebrew.
* [pip](http://pypi.python.org/pypi/pip).
* [virtualenv](http://pypi.python.org/pypi/virtualenv).
* [virtualenvwrapper](http://www.doughellmann.com/docs/virtualenvwrapper/).

**Note:** There is an issue installing lxml with Xcode 4, which is not
  required to run the Pylons app, but is required to run the
  tests. See https://gist.github.com/963298 for instructions on
  manually installing lxml with Xcode 4.

## Installation ##
* Clone this repository. If you are viewing this page on github, you
  should see the clone URL near the top of the page.

>       git clone <repository URL>

* Install CouchDB using Homebrew.

>       brew install couchdb

* Create a virtualenv for Learning Registry.

>       mkvirtualenv --no-site-packages --distribute learning-registry

* Install the required python packages into the virtualenv. The
  `mkvirtualenv` command will automatically activate the newly created
  virtualenv.

>       pip install pylons pyparsing couchdb restkit lxml iso8601plus

* Change directory to the root of the cloned Learning Registry git repository.

>       cd <path to clone of the git repository>

* Install the Learning Registry pylons app.

>       cd LR
>       pip install -e .

## Setup ##
* Start up couchdb

>       launchctl load -w /usr/local/Cellar/couchdb/1.0.2/Library/LaunchDaemons/org.apache.couchdb.plist

* Change directory to the root of the cloned Learning Registry git repository.

>       cd <path to clone of the git repository>

* Create a development configuration file. You may copy the original
  configuration file in the LR directory.

>       cp LR/development.ini.orig LR/development.ini

* Navigate to the `config` directory within your clone of the Learning
  Registry git repository.

>       cd config

* Load the initial documents for Learning Registry into CouchDB. This
  script will ask a few questions.

>       ./setup_node.py

* Edit the development.ini file and replace the line
  `use = egg:Flup#fcgi_thread` with `use = egg:Paste#http`.

## Start up the node ##
* Run the development web server.

>       paster serve --reload development.ini

* Check to see if all is well by checking the status of the node we
  have just set up. You should receive a response if it's working.

>       curl -i http://127.0.0.1:5000/status


  
