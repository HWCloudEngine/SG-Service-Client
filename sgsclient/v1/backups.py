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


class Backup(base.Resource):
    def __repr__(self):
        return "<Backup %s>" % self._info


class BackupManager(base.ManagerWithFind):
    resource_class = Backup

    def create(self, volume_id, name=None, description=None, type='full',
               destination='local'):
        body = {'backup': {"volume_id": volume_id,
                           "name": name,
                           "description": description,
                           "type": type,
                           'destination': destination}}
        url = "/backups"
        return self._create(url, body, 'backup')

    def list(self, detailed=False, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, sort=None):
        """Lists all backups.

        :param detailed: Whether to return detailed volume info.
        :param search_opts: Search options to filter out backups.
        :param marker: Begin returning backups that appear later in the
                       backup list than that represented by this id.
        :param limit: Maximum number of backups to return.
        :param sort_key: Key to be sorted; deprecated in kilo
        :param sort_dir: Sort direction, should be 'desc' or 'asc'; deprecated
                         in kilo
        :param sort: Sort information
        :rtype: list of :class:`Backup`
        """
        resource_type = "backups"
        url = self._build_list_url(
            resource_type, detailed=detailed,
            search_opts=search_opts, marker=marker,
            limit=limit, sort_key=sort_key,
            sort_dir=sort_dir, sort=sort)
        return self._list(url, 'backups')

    def update(self, backup_id, **kwargs):
        if not kwargs:
            return
        body = {"backup": kwargs}
        return self._update('/backups/{backup_id}'
                            .format(backup_id=backup_id),
                            body, "backup")

    def delete(self, backup_id):
        path = '/backups/{backup_id}'.format(
            backup_id=backup_id)
        return self._delete(path)

    def get(self, backup_id, session_id=None):
        if session_id:
            headers = {'X-Configuration-Session': session_id}
        else:
            headers = {}
        url = "/backups/{backup_id}".format(
            backup_id=backup_id)
        return self._get(url, response_key="backup", headers=headers)

    def restore(self, backup_id, volume_id):
        action_data = {"volume_id": volume_id}
        url = "/backups/{backup_id}/action".format(backup_id=backup_id)
        return self._action('restore', url, action_data,
                            response_key='restore')

    def export_record(self, backup_id):
        url = "/backups/{backup_id}/action".format(backup_id=backup_id)
        return self._action('export_record', url, response_key='backup_record')

    def import_record(self, backup_record):
        data = {'backup_record': backup_record}
        url = "/backups/import_record"
        return self._create(url, data, response_key='backup')

    def reset_state(self, backup_id, state):
        action_data = {'status': state}
        url = "/backups/{backup_id}/action".format(backup_id=backup_id)
        return self._action('reset_status', url, action_data)
