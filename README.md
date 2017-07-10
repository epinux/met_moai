# met_moai

met.no's extension for moai (https://github.com/infrae/moai), allowing
the exposure of our metadata in various other formats.

## Setup and running

To set up and run manually:

You need the following debian-packages:

  * python-pip
  * libxml2-dev
  * libxslt-dev
  * zlib1g-dev
  * virtualenv

From top source directory:

$ virtualenv deps
$ . deps/bin/activate
$ python setup.py develop

Update etc/mmd_config.ini and etc/settings.ini (see below). At least
modify database in settings.ini.

$ bin/update.sh
$ bin/run.sh

Metadata updates are in this setup not automatic. You must
periodically run bin/update.sh to get recent updates.

For running after the first time:

$ . deps/bin/activate
$ bin/run.sh

Data should then be available in your browser like this
http://localhost:8080/oai?verb=ListMetadataFormats


## Configuration files

You will need to check and possibly modify the following files:

###  etc/mmd_config.ini

This file contains configuration for available transformations. You
should normally not need to edit this one.

If you add a new entry, you must also add a new entry in setup.py's
entry_point moai.format, and in etc/settings.ini.

### etc/settings.ini

This is the main configuration file for moai. Relevant entries to
modify here are the follwing:

  * url: The advertised host name. Must equal the base address you use
    when connecting to the service. For local installations,
    http://localhost:8080 is a fine default.

  * formats: The data formats to expose

  * database: Name of a file to store metadata. Must be writeable by
    the user running met_moai.

