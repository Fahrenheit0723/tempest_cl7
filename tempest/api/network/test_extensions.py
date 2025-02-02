# Copyright 2013 OpenStack, Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from tempest.api.network import base
from tempest.common import utils
from tempest.lib import decorators


class ExtensionsTestJSON(base.BaseNetworkTest):
    """Tests the following operations in the Neutron API:

        List all available extensions

    v2.0 of the Neutron API is assumed. It is also assumed that api-extensions
    option is defined in the [network-feature-enabled] section of
    etc/tempest.conf.
    """

    @decorators.idempotent_id('ef28c7e6-e646-4979-9d67-deb207bc5564')
    def test_list_show_extensions(self):
        """List available extensions and show the detail of each extension"""
        expected_alias = ['security-group', 'l3_agent_scheduler',
                          'ext-gw-mode', 'binding', 'quotas',
                          'agent', 'dhcp_agent_scheduler', 'provider',
                          'router', 'extraroute', 'external-net',
                          'allowed-address-pairs', 'extra_dhcp_opt',
                          'metering', 'dvr']
        expected_alias = [ext for ext in expected_alias if
                          utils.is_extension_enabled(ext, 'network')]
        actual_alias = list()
        extensions = self.network_extensions_client.list_extensions()
        list_extensions = extensions['extensions']
        # Show and verify the details of the available extensions
        for ext in list_extensions:
            ext_name = ext['name']
            ext_alias = ext['alias']
            actual_alias.append(ext['alias'])
            ext_details = self.network_extensions_client.show_extension(
                ext_alias)
            ext_details = ext_details['extension']

            self.assertIsNotNone(ext_details)
            self.assertIn('updated', ext_details.keys())
            self.assertIn('name', ext_details.keys())
            self.assertIn('description', ext_details.keys())
            self.assertIn('links', ext_details.keys())
            self.assertIn('alias', ext_details.keys())
            self.assertEqual(ext_details['name'], ext_name)
            self.assertEqual(ext_details['alias'], ext_alias)
            self.assertEqual(ext_details, ext)
        # Verify if expected extensions are present in the actual list
        # of extensions returned, but only for those that have been
        # enabled via configuration
        for e in expected_alias:
            if utils.is_extension_enabled(e, 'network'):
                self.assertIn(e, actual_alias)
