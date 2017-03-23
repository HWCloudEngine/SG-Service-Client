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

from sgsclient import base
from sgsclient.v1.volumes import Volume


class ReplicateManager(base.Manager):
    resource_class = Volume

    def create(self, volume_id, mode, replication_id, peer_volume):
        action_data = {'mode': mode,
                       'replication_id': replication_id,
                       'peer_volume': peer_volume}
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("create_replicate", url, action_data, 'replicate')

    def delete(self, volume_id):
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("delete_replicate", url)

    def enable(self, volume_id):
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("enable_replicate", url, response_key='replicate')

    def disable(self, volume_id):
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("disable_replicate", url, response_key='replicate')

    def failover(self, volume_id, checkpoint_id=None, force=False):
        action_data = {'checkpoint_id': checkpoint_id,
                       'force': force}
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("failover_replicate", url, action_data,
                            'replicate')

    def reverse(self, volume_id):
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        return self._action("reverse_replicate", url, response_key='replicate')
