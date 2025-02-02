# Copyright 2013 OpenStack Foundation
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

from tempest.api.identity import base
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators


class PoliciesTestJSON(base.BaseIdentityV3AdminTest):
    """Test keystone policies"""

    def _delete_policy(self, policy_id):
        self.policies_client.delete_policy(policy_id)

    @decorators.idempotent_id('1a0ad286-2d06-4123-ab0d-728893a76201')
    def test_list_policies(self):
        """Test to list keystone policies"""
        policy_ids = list()
        fetched_ids = list()
        for _ in range(3):
            blob = data_utils.rand_name('BlobName')
            policy_type = data_utils.rand_name('PolicyType')
            policy = self.policies_client.create_policy(
                blob=blob, type=policy_type)['policy']
            # Delete the Policy at the end of this method
            self.addCleanup(self._delete_policy, policy['id'])
            policy_ids.append(policy['id'])
        # List and Verify Policies
        body = self.policies_client.list_policies()['policies']
        for p in body:
            fetched_ids.append(p['id'])
        missing_pols = [p for p in policy_ids if p not in fetched_ids]
        self.assertEmpty(missing_pols)


    @decorators.idempotent_id('e544703a-2f03-4cf2-9b0f-350782fdb0d3')
    def test_create_update_delete_policy(self):
        """Test to update keystone policy"""
        blob = data_utils.rand_name('BlobName')
        policy_type = data_utils.rand_name('PolicyType')
        policy = self.policies_client.create_policy(blob=blob,
                                                    type=policy_type)['policy']
        self.addCleanup(self._delete_policy, policy['id'])
        self.assertIn('type', policy)
        self.assertIn('blob', policy)
        self.assertIsNotNone(policy['id'])
        self.assertEqual(blob, policy['blob'])
        self.assertEqual(policy_type, policy['type'])
        # Update policy
        update_type = data_utils.rand_name('UpdatedPolicyType')
        data = self.policies_client.update_policy(
            policy['id'], type=update_type)['policy']
        self.assertIn('type', data)
        # Assertion for updated value with fetched value
        fetched_policy = self.policies_client.show_policy(
            policy['id'])['policy']
        self.assertIn('id', fetched_policy)
        self.assertIn('blob', fetched_policy)
        self.assertIn('type', fetched_policy)
        self.assertEqual(fetched_policy['id'], policy['id'])
        self.assertEqual(fetched_policy['blob'], policy['blob'])
        self.assertEqual(update_type, fetched_policy['type'])
