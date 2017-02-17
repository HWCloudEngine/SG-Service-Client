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


class Snapshot(base.Resource):
    def __repr__(self):
        return "<Snapshot %s>" % self._info


class SnapshotManager(base.ManagerWithFind):
    resource_class = Snapshot

    def create(self, volume_id, name=None, description=None, checkpoint_id=None):
        body = {'snapshot': {"volume_id": volume_id,
                             "name": name,
                             "description": description,
                             "checkpoint_id": checkpoint_id}}
        url = "/snapshots"
        return self._create(url, body, 'snapshot')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all snapshots.

        :param detailed: Whether to return detailed volume info.
        :param search_opts: Search options to filter out snapshots.
        :param marker: Begin returning snapshots that appear later in the
                       snapshot list than that represented by this id.
        :param limit: Maximum number of snapshots to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Snapshot`
        """
        resource_type = "snapshots"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'snapshots')

    def update(self, snapshot_id, data):
        body = {"snapshot": data}
        return self._update('/snapshots/{snapshot_id}'
                            .format(snapshot_id=snapshot_id),
                            body, "snapshot")

    def delete(self, snapshot_id):
        path = '/snapshots/{snapshot_id}'.format(
            snapshot_id=snapshot_id)
        return self._delete(path)

    def get(self, snapshot_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/snapshots/{snapshot_id}".format(
            snapshot_id=snapshot_id)
        return self._get(url, response_key="snapshot", headers=headers)
