Paasmaker Python Interface Library
==================================

This is a simple Python library that is designed to read in the Paasmaker
configuration, falling back to a custom configuration file in development.

Usage
-----

In the startup of your application create an interface object. Supply the
constructor with a list of locations to look for override configuration
files for development.

	import pminterface

	interface = pminterface.PaasmakerInterface(['../my-project.yml'])

	interface.is_on_paasmaker() # Returns true if on Paasmaker.

	# Raises NameError if no such service exists.
	service = interface.get_service('named-service')
	# service now is a dict of the parameters. Typically this will
	# have the keys 'hostname', 'username', 'password', etc. Use this
	# to connect to revelant services.

	# Get other application metadata.
	application = interface.get_application_name()

Override configuration files can be in either YAML or JSON format. If using
the YAML format, be sure to install pyyaml first. If pyyaml isn't present,
only the JSON format is supported, and it will raise an exception when
trying to read YAML files.

Example YAML configuration file:

	services:
	  parameters:
	    foo: bar

	application:
	  name: test
	  version: 1
	  workspace: Test
	  workspace_stub: test

Example JSON configuration file:

	{
		"services": {
			"parameters": {
				"foo": "bar"
			}
		},
		"application": {
			"name": "test",
			"version": 1,
			"workspace": "Test",
			"workspace_stub": "test"
		}
	}