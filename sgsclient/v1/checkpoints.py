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


class Checkpoint(base.Resource):
    def __repr__(self):
        return "<Checkpoint %s>" % self._info


class CheckpointManager(base.ManagerWithFind):
    resource_class = Checkpoint

    def create(self, replication_id, name=None, description=None):
        body = {'checkpoint': {"replication_id": replication_id,
                               "name": name,
                               "description": description}}
        url = "/checkpoints"
        return self._create(url, body, 'checkpoint')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all checkpoints.

        :param detailed: Whether to return detailed checkpoint info.
        :param search_opts: Search options to filter out checkpoints.
        :param marker: Begin returning checkpoints that appear later in the
                       checkpoint list than that represented by this id.
        :param limit: Maximum number of checkpoints to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Checkpoint`
        """
        resource_type = "checkpoints"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'checkpoints')

    def update(self, checkpoint_id, data):
        body = {"checkpoint": data}
        return self._update('/checkpoints/{checkpoint_id}'
                            .format(checkpoint_id=checkpoint_id),
                            body, "checkpoint")

    def delete(self, checkpoint_id):
        path = '/checkpoints/{checkpoint_id}'.format(
            checkpoint_id=checkpoint_id)
        return self._delete(path)

    def get(self, checkpoint_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/checkpoints/{checkpoint_id}".format(
            checkpoint_id=checkpoint_id)
        return self._get(url, response_key="checkpoint", headers=headers)

    def rollback(self, checkpoint_id):
        url = "/checkpoints/{checkpoint_id}/rollback".format(
            checkpoint_id=checkpoint_id)
        body = None
        return self._create(url, body, 'rollback')
