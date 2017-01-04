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


class Replication(base.Resource):
    def __repr__(self):
        return "<Replication %s>" % self._info


class ReplicationManager(base.ManagerWithFind):
    resource_class = Replication

    def create(self, name, master_volume, slave_volume, description=None):
        body = {'replication': {'name': name,
                                'master_volume': master_volume,
                                'slave_volume': slave_volume,
                                'description': description
                                }}
        url = "/replications"
        return self._create(url, body, 'replication')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all replications.

        :param detailed: Whether to return detailed volume info.
        :param search_opts: Search options to filter out replications.
        :param marker: Begin returning replications that appear later in the
                       replication list than that represented by this id.
        :param limit: Maximum number of replications to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Replication`
        """
        resource_type = "replications"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'replications')

    def update(self, replication_id, data):
        body = {"replication": data}
        return self._update('/replications/{replication_id}'
                            .format(replication_id=replication_id),
                            body, "replication")

    def delete(self, replication_id):
        path = '/replications/{replication_id}'.format(
            replication_id=replication_id)
        return self._delete(path)

    def get(self, replication_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/replications/{replication_id}".format(
            replication_id=replication_id)
        return self._get(url, response_key="replication", headers=headers)

    def enable(self, replication_id):
        return self._action("enable", replication_id)

    def disable(self, replication_id):
        return self._action("disable", replication_id)

    def failover(self, replication_id):
        return self._action("failover", replication_id)

    def reverse(self, replication_id):
        return self._action("reverse", replication_id)

    def _action(self, action, replication_id, info=None):
        """Perform a replication "action."
        """
        data = {action: info}
        url = "/replications/{replication_id}/action".format(
            replication_id=replication_id)
        resp, body = self.api.json_request('POST', url, data=data)

        if body is not None:
            return self.resource_class(self, body["replication"])
