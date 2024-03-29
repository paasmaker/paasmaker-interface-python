#!/usr/bin/env python

# Copyright (c) 2013 Daniel Foote.
#
# See the file LICENSE for copying permission.

import unittest
import os
import json

import pminterface

class PaasmakerInterfaceTest(unittest.TestCase):

	def tearDown(self):
		# Clean up any environment from the test.
		if 'PM_SERVICES' in os.environ:
			del os.environ['PM_SERVICES']
		if 'PM_METADATA' in os.environ:
			del os.environ['PM_METADATA']
		if 'PM_PORT' in os.environ:
			del os.environ['PM_PORT']

		super(PaasmakerInterfaceTest, self).tearDown()

	def test_simple(self):
		# Give it no configuration paths.
		try:
			interface = pminterface.PaasmakerInterface([])
			self.assertTrue(False, "Should have thrown exception.")
		except pminterface.PaasmakerInterfaceError, ex:
			self.assertTrue(True, "Threw exception correctly.")

		# Now give it a path that does not exist.
		try:
			interface = pminterface.PaasmakerInterface(['configs/noexist.yml'])
			self.assertTrue(False, "Should have thrown exception.")
		except pminterface.PaasmakerInterfaceError, ex:
			self.assertTrue(True, "Threw exception correctly.")

		# Finally, give it a path that doesn't exist then one that does.
		interface = pminterface.PaasmakerInterface(['configs/noexist.yml', 'configs/test.yml'])
		# And this should not raise an exception.

		self.assertEquals(interface.get_port(), 9002)

	def test_json_config(self):
		interface = pminterface.PaasmakerInterface(['configs/test.json'])

		self._confirm_test_configuration(interface)

	def test_yml_config(self):
		interface = pminterface.PaasmakerInterface(['configs/test.yml'])

		self._confirm_test_configuration(interface)

	def test_invalid_config(self):
		try:
			interface = pminterface.PaasmakerInterface(['configs/invalid.yml'])
			self.assertTrue(False, "Should have thrown exception.")
		except pminterface.PaasmakerInterfaceError, ex:
			self.assertTrue(True, "Threw exception correctly.")

		try:
			interface = pminterface.PaasmakerInterface(['configs/invalid2.yml'])
			self.assertTrue(False, "Should have thrown exception.")
		except pminterface.PaasmakerInterfaceError, ex:
			self.assertTrue(True, "Threw exception correctly.")

	def test_tags(self):
		interface = pminterface.PaasmakerInterface(['configs/tags.yml'])

		workspace_tags = interface.get_workspace_tags()
		node_tags = interface.get_node_tags()
		self.assertTrue('tag' in workspace_tags)
		self.assertTrue('tag' in node_tags)

	def test_paasmaker_config(self):
		# Generate and insert the configuration into the environment.
		services_raw = {'variables': {'one': 'two'}}
		metadata_raw = {
			'application': {
				'name': 'test',
				'version': 1,
				'workspace': 'Test',
				'workspace_stub': 'test'
			},
			'node': {'one': 'two'},
			'workspace': {'three': 'four'}
		}

		os.environ['PM_SERVICES'] = json.dumps(services_raw)
		os.environ['PM_METADATA'] = json.dumps(metadata_raw)
		os.environ['PM_PORT'] = "42600"

		interface = pminterface.PaasmakerInterface([])

		self.assertTrue(interface.is_on_paasmaker())
		self.assertEquals(interface.get_application_name(), "test")
		self.assertEquals(interface.get_application_version(), 1)
		self.assertEquals(interface.get_workspace_name(), "Test")
		self.assertEquals(interface.get_workspace_stub(), "test")

		workspace_tags = interface.get_workspace_tags()
		node_tags = interface.get_node_tags()
		self.assertTrue('three' in workspace_tags)
		self.assertTrue('one' in node_tags)

		service = interface.get_service('variables')
		self.assertTrue('one' in service)

		self.assertEquals(interface.get_port(), 42600)

		try:
			interface.get_service('no-service')
			self.assertTrue(False, "Should have thrown exception.")
		except NameError, ex:
			self.assertTrue(True, "Threw exception correctly.")

	def _confirm_test_configuration(self, interface):
		self.assertFalse(interface.is_on_paasmaker(), "Should not think it's on paasmaker.")
		self.assertEquals(interface.get_application_name(), "test")
		self.assertEquals(interface.get_application_version(), 1)
		self.assertEquals(interface.get_workspace_name(), "Test")
		self.assertEquals(interface.get_workspace_stub(), "test")
		self.assertEquals(len(interface.get_workspace_tags()), 0)
		self.assertEquals(len(interface.get_node_tags()), 0)
		self.assertEquals(len(interface.get_all_services()), 1)

		service = interface.get_service('parameters')
		self.assertTrue('foo' in service)

		try:
			interface.get_service('no-service')
			self.assertTrue(False, "Should have thrown exception.")
		except NameError, ex:
			self.assertTrue(True, "Threw exception correctly.")

if __name__ == '__main__':
	unittest.main()