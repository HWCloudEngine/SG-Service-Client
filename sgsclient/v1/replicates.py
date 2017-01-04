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

from sgsclient.common import base
from sgsclient.v1.volumes import Volume


class ReplicateManager(base.Manager):
    resource_class = Volume

    def create(self, volume_id, mode, peer_volume):
        info = {'mode': mode,
                'peer_volume': peer_volume}
        return self._action("create_replicate", volume_id, info)

    def delete(self, volume_id):
        return self._action("delete_replicate", volume_id)

    def enable(self, volume_id):
        return self._action("enable_replicate", volume_id)

    def disable(self, volume_id):
        return self._action("disable_replicate", volume_id)

    def failover(self, volume_id):
        return self._action("failover_replicate", volume_id)

    def reverse(self, volume_id):
        return self._action("reverse_replicate", volume_id)

    def _action(self, action, volume_id, info=None):
        """Perform a replicate "action."
        """
        data = {action: info}
        url = "/volume_replicate/{volume_id}/action".format(
            volume_id=volume_id)
        resp, body = self.api.json_request('POST', url, data=data)

        if body is not None:
            return self.resource_class(self, body["volume"])
