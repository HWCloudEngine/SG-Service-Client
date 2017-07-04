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


class Volume(base.Resource):
    def __repr__(self):
        return "<Volume %s>" % self._info


class VolumeManager(base.ManagerWithFind):
    resource_class = Volume

    def create(self, snapshot_id=None, checkpoint_id=None, volume_type=None,
               availability_zone=None, name=None, description=None,
               volume_id=None, size=None):
        body = {'volume': {'name': name,
                           'snapshot_id': snapshot_id,
                           'checkpoint_id': checkpoint_id,
                           'description': description,
                           'volume_type': volume_type,
                           'availability_zone': availability_zone,
                           'volume_id': volume_id,
                           'size': size}}
        url = "/volumes"
        return self._create(url, body, 'volume')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all volumes.

        :param detailed: Whether to return detailed volume info.
        :param search_opts: Search options to filter out volumes.
        :param marker: Begin returning volumes that appear later in the
                       volume list than that represented by this id.
        :param limit: Maximum number of volumes to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Volume`
        """
        resource_type = "volumes"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'volumes')

    def update(self, volume_id, **kwargs):
        if not kwargs:
            return
        body = {"volume": kwargs}
        return self._update('/volumes/{volume_id}'
                            .format(volume_id=volume_id),
                            body, "volume")

    def delete(self, volume_id):
        path = '/volumes/{volume_id}'.format(
            volume_id=volume_id)
        return self._delete(path)

    def get(self, volume_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/volumes/{volume_id}".format(
            volume_id=volume_id)
        return self._get(url, response_key="volume", headers=headers)

    def enable(self, volume_id, name=None, description=None, metadata=None):
        action_data = {
            'name': name,
            'description': description,
            'metadata': metadata
        }
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        return self._action("enable", url, action_data, 'volume')

    def disable(self, volume_id):
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        return self._action("disable", url, response_key='volume')

    def attach(self, volume_id, instance_uuid, mode='rw'):
        action_data = {
            'instance_uuid': instance_uuid,
            'mode': mode
        }
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        return self._action("attach", url, action_data, response_key='attach')

    def detach(self, volume_id, instance_uuid):
        action_data = {
            "instance_uuid": instance_uuid
        }
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        return self._action("detach", url, action_data)

    def reset_state(self, volume_id, state):
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        action_data = {'status': state}
        return self._action('reset_status', url, action_data)
