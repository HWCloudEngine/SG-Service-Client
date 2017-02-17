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


class Volume(base.Resource):
    def __repr__(self):
        return "<Volume %s>" % self._info


class VolumeManager(base.ManagerWithFind):
    resource_class = Volume

    def create(self, snapshot_id=None, checkpoint_id=None, volume_type=None,
               availability_zone=None, name=None, description=None):
        body = {'volume': {'name': name,
                           'snapshot_id': snapshot_id,
                           'checkpoint_id': checkpoint_id,
                           'description': description,
                           'volume_type': volume_type,
                           'availability_zone': availability_zone,
                           }}
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

    def update(self, volume_id, data):
        body = {"volume": data}
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

    def enable(self, volume_id, name=None, description=None):
        info = {
            'name': name,
            'description': description
        }
        return self._action("enable", volume_id, info)

    def disable(self, volume_id):
        return self._action("disable", volume_id)

    def reserve(self, volume_id):
        return self._action("reserve", volume_id)

    def unreserve(self, volume_id):
        return self._action("unreserve", volume_id)

    def initialize_connection(self, volume_id):
        return self._action("initialize_connection", volume_id,
                            response_key="connection_info")

    def attach(self, volume_id, instance_uuid, mountpoint, mode='rw',
               host_name=None):
        info = {
            'instance_uuid': instance_uuid,
            'mountpoint': mountpoint,
            'mode': mode,
            'host_name': host_name
        }
        return self._action("attach", volume_id, info=info)

    def begin_detaching(self, volume_id):
        return self._action("begin_detaching", volume_id)

    def roll_detaching(self, volume_id):
        return self._action("roll_detaching", volume_id)

    def detach(self, volume_id, attachment_uuid=None):
        info = {
            "attachment_uuid": attachment_uuid
        }
        return self._action("detach", volume_id, info=info)

    def _action(self, action, volume_id, info=None, response_key="volume"):
        """Perform a volume "action."
        """
        data = {action: info}
        url = "/volumes/{volume_id}/action".format(volume_id=volume_id)
        resp, body = self.api.json_request('POST', url, data=data)

        if body is not None:
            return self.resource_class(self, body[response_key])
