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

import sys
import time

from sgsclient import utils


def find_volume(cs, volume):
    """Gets a volume by name or ID."""
    return utils.find_resource(cs.volumes, volume)


def find_backup(cs, backup):
    """Gets a backup by name or ID."""
    return utils.find_resource(cs.backups, backup)


def find_snapshot(cs, snapshot):
    """Gets a snapshot by name or ID."""
    return utils.find_resource(cs.snapshots, snapshot)


def find_replication(cs, replication):
    """Gets a replication by name or ID."""
    return utils.find_resource(cs.replications, replication)


def find_checkpoint(cs, checkpoint):
    """Gets a checkpoint by name or ID."""
    return utils.find_resource(cs.checkpoints, checkpoint)
