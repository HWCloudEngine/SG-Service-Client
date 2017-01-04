#    Copyright (c) 2013 Mirantis, Inc.
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

from sgsclient.common import http
from sgsclient.v1 import backups
from sgsclient.v1 import replicates
from sgsclient.v1 import replications
from sgsclient.v1 import snapshots
from sgsclient.v1 import volumes

class Client(object):
    """Client for the sgs v1 API.

    :param string endpoint: A user-supplied endpoint URL for the service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the sgs v1 API."""
        self.http_client = http._construct_http_client(*args, **kwargs)
        self.replications = replications.ReplicationManager(self.http_client)
        self.volumes = volumes.VolumeManager(self.http_client)
        self.replicates = replicates.ReplicateManager(self.http_client)
        self.backups = backups.BackupManager(self.http_client)
        self.snapshots = snapshots.SnapshotManager(self.http_client)
