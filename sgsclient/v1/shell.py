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

import argparse
import os

from oslo_serialization import jsonutils
from sgsclient import base
from sgsclient import exceptions
from sgsclient import shell_utils
from sgsclient import utils


#################

@utils.arg('master_volume',
           metavar='<master-volume>',
           help='ID of master-volume.')
@utils.arg('slave_volume',
           metavar='<slave-volume>',
           help='ID of slave-volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Replication name.')
@utils.arg('--description',
           metavar='<description>',
           help='The description of a replication.')
def do_replication_create(cs, args):
    """Create a replication."""
    replication = cs.replications.create(
        args.master_volume, args.slave_volume, name=args.name,
        description=args.description)
    utils.print_dict(replication.to_dict())


@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of replication.')
def do_replication_enable(cs, args):
    """Enable a replication."""
    replication = shell_utils.find_replication(cs, args.replication)
    replication = cs.replications.enable(replication.id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of replication.')
def do_replication_disable(cs, args):
    """Disable a replication."""
    replication = shell_utils.find_replication(cs, args.replication)
    replication = cs.replications.disable(replication.id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of replication.')
@utils.arg('--force',
           action='store_true',
           default=False,
           help='Force to failover replication')
def do_replication_failover(cs, args):
    """Failover a replication."""
    replication = shell_utils.find_replication(cs, args.replication)
    replication = cs.replications.failover(replication.id, args.force)
    utils.print_dict(replication.to_dict())


@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of replication.')
def do_replication_reverse(cs, args):
    """Reverse a replication."""
    replication = shell_utils.find_replication(cs, args.replication)
    replication = cs.replications.reverse(replication.id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication',
           metavar='<replication>', nargs='+',
           help='ID or name of replication.')
def do_replication_delete(cs, args):
    """Delete a replication."""
    failure_count = 0
    for item in args.replication:
        try:
            replication = shell_utils.find_replication(cs, item)
            cs.replications.delete(replication.id)
            print("Request to delete replication %s has been accepted." % item)
        except Exception as e:
            failure_count += 1
            print("Delete for replication %s failed: %s" % (item, e))
    if failure_count == len(args.replication):
        raise exceptions.CommandError("Unable to delete any of the specified "
                                      "replications.")


@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of replication.')
def do_replication_show(cs, args):
    """Get a replication."""
    replication = shell_utils.find_replication(cs, args.replication)
    utils.print_dict(replication.to_dict())


@utils.arg('--all-tenants',
           dest='all_tenants',
           metavar='<0|1>',
           nargs='?',
           type=int,
           const=1,
           default=0,
           help='Shows details for all tenants. Admin only.')
@utils.arg('--all_tenants',
           nargs='?',
           type=int,
           const=1,
           help=argparse.SUPPRESS)
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning plans that appear later in the plan '
                'list than that represented by this plan id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of plans to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort',
           metavar='<key>[:<direction>]',
           default=None,
           help=(('Comma-separated list of sort keys and directions in the '
                  'form of <key>[:<asc|desc>]. '
                  'Valid keys: %s. '
                  'Default=None.') % ', '.join(base.SORT_KEY_VALUES)))
@utils.arg('--tenant',
           type=str,
           dest='tenant',
           nargs='?',
           metavar='<tenant>',
           help='Display information from single tenant (Admin only).')
def do_replication_list(cs, args):
    """list volumes."""
    all_tenants = 1 if args.tenant else \
        int(os.environ.get("ALL_TENANTS", args.all_tenants))
    search_opts = {
        'all_tenants': all_tenants,
        'project_id': args.tenant,
        'name': args.name,
        'status': args.status,
    }

    if args.sort and (args.sort_key or args.sort_dir):
        raise exceptions.CommandError(
            'The --sort_key and --sort_dir arguments are deprecated and are '
            'not supported with --sort.')

    replications = cs.replications.list(search_opts=search_opts,
                                        marker=args.marker,
                                        limit=args.limit,
                                        sort_key=args.sort_key,
                                        sort_dir=args.sort_dir, sort=args.sort)
    columns = ['Id', 'Name', 'Status', 'Master volume', 'Slave volume']

    if args.sort_key or args.sort_dir or args.sort:
        sortby_index = None
    else:
        sortby_index = 0
    utils.print_list(replications, columns, exclude_unavailable=True,
                     sortby_index=sortby_index)


@utils.arg('replication', metavar='<replication>',
           help='ID of the replication to modify.')
@utils.arg('--state', metavar='<state>',
           default='enabled',
           help='The state to assign to the replication.')
def do_replication_reset_state(cs, args):
    replication = args.replication
    try:
        cs.replications.reset_state(replication, args.state)
        print("Request to reset-state replication %s has been accepted." % (
            replication))
    except Exception as e:
        print("Reset-state for replication %s failed: %s" % (replication, e))


@utils.arg('replication',
           metavar='<replication>',
           help='Name or ID of replication to update.')
@utils.arg('--name',
           nargs='?',
           metavar='<name>',
           help='New name for replication.')
@utils.arg('--description',
           nargs='?',
           metavar='<description>',
           help='New description for replication.')
def do_replication_update(cs, args):
    kwargs = {}
    if args.name is not None:
        kwargs['name'] = args.name
    if args.description is not None:
        kwargs['description'] = args.description

    if not kwargs:
        msg = 'Must supply either name or description.'
        raise exceptions.ClientException(code=1, message=msg)

    replication = shell_utils.find_replication(cs, args.replication)
    replication = cs.replications.update(replication.id, kwargs)
    utils.print_dict(replication.to_dict())


################

@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_show(cs, args):
    """Get a volume."""
    volume = shell_utils.find_volume(cs, args.volume)
    utils.print_dict(volume.to_dict())


@utils.arg('--all-tenants',
           dest='all_tenants',
           metavar='<0|1>',
           nargs='?',
           type=int,
           const=1,
           default=0,
           help='Shows details for all tenants. Admin only.')
@utils.arg('--all_tenants',
           nargs='?',
           type=int,
           const=1,
           help=argparse.SUPPRESS)
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning plans that appear later in the plan '
                'list than that represented by this plan id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of plans to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort',
           metavar='<key>[:<direction>]',
           default=None,
           help=(('Comma-separated list of sort keys and directions in the '
                  'form of <key>[:<asc|desc>]. '
                  'Valid keys: %s. '
                  'Default=None.') % ', '.join(base.SORT_KEY_VALUES)))
@utils.arg('--tenant',
           type=str,
           dest='tenant',
           nargs='?',
           metavar='<tenant>',
           help='Display information from single tenant (Admin only).')
def do_list(cs, args):
    """list volumes."""
    all_tenants = 1 if args.tenant else \
        int(os.environ.get("ALL_TENANTS", args.all_tenants))
    search_opts = {
        'all_tenants': all_tenants,
        'project_id': args.tenant,
        'name': args.name,
        'status': args.status,
    }

    if args.sort and (args.sort_key or args.sort_dir):
        raise exceptions.CommandError(
            'The --sort_key and --sort_dir arguments are deprecated and are '
            'not supported with --sort.')

    volumes = cs.volumes.list(search_opts=search_opts, marker=args.marker,
                              limit=args.limit, sort_key=args.sort_key,
                              sort_dir=args.sort_dir, sort=args.sort)
    columns = ['Id', 'Name', 'Status', 'Replicate Status', 'Replicate Mode']

    if args.sort_key or args.sort_dir or args.sort:
        sortby_index = None
    else:
        sortby_index = 0
    utils.print_list(volumes, columns, exclude_unavailable=True,
                     sortby_index=sortby_index)


@utils.arg('--checkpoint-id',
           metavar='<checkpoint-id>',
           help='ID of checkpoint.')
@utils.arg('--snapshot-id',
           metavar='<snapshot-id>',
           help='ID of snapshot.')
@utils.arg('--name',
           metavar='<name>',
           help='Volume name.')
@utils.arg('--description',
           metavar='<description>',
           help='The description of volume.')
@utils.arg('--volume-type',
           metavar='<volume-type>',
           help='Volume type.')
@utils.arg('--availability-zone',
           metavar='<availability-zone>',
           help='availability zone')
@utils.arg('--size',
           metavar='<size>',
           help='size')
@utils.arg('--volume-id',
           metavar='<volume-id>',
           help='The new available cinder volume')
def do_create_volume(cs, args):
    """Create a volume from snapshot, or copy snapshot to a volume."""
    if [args.checkpoint_id, args.snapshot_id] == [None, None]:
        print ("create volume must specify a checkpoint or snapshot")
        return
    volume = cs.volumes.create(checkpoint_id=args.checkpoint_id,
                               snapshot_id=args.snapshot_id,
                               name=args.name,
                               description=args.description,
                               volume_type=args.volume_type,
                               availability_zone=args.availability_zone,
                               size=args.size,
                               volume_id=args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Replication name.')
@utils.arg('--description',
           metavar='<description>',
           help='The description of a replication.')
@utils.arg('--metadata',
           action='append',
           metavar='key=val[,key=val,...]',
           default=[],
           help='Metadata info.')
def do_enable_sg(cs, args):
    """Enable volume's SG."""
    metadata = _extract_metadata(args)
    volume = cs.volumes.enable(args.volume_id, args.name, args.description,
                               metadata)
    utils.print_dict(volume.to_dict())


def _extract_metadata(args):
    if not args.metadata:
        return {}

    metadata = {}
    for resource_params in args.metadata:
        for param_kv in resource_params.split(','):
            key, value = param_kv.split('=')
            metadata[key] = value
    return metadata


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_disable_sg(cs, args):
    """Disable volume's SG."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.volumes.disable(volume.id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='Name or ID of volume to update.')
@utils.arg('--name',
           nargs='?',
           metavar='<name>',
           help='New name for volume.')
@utils.arg('--description',
           nargs='?',
           metavar='<description>',
           help='New description for volume.')
def do_update(cs, args):
    kwargs = {}
    if args.name is not None:
        kwargs['name'] = args.name
    if args.description is not None:
        kwargs['description'] = args.description

    if not kwargs:
        msg = 'Must supply either name or description.'
        raise exceptions.ClientException(code=1, message=msg)

    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.volumes.update(volume.id, kwargs)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('instance_uuid',
           metavar='<instance-uuid>',
           help='ID of instance.')
@utils.arg('--mode',
           metavar='<mode>',
           help='The attach mode.')
def do_attach(cs, args):
    """Add sg-volume attachment metadata."""
    mode = args.mode
    mode = 'rw' if mode is None else mode
    if mode not in ['rw', 'ro']:
        print("Attach mode must be rw or ro")
        return
    volume = shell_utils.find_volume(cs, args.volume)
    attach = cs.volumes.attach(volume.id, args.instance_uuid, mode)
    utils.print_dict(attach.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('instance_uuid',
           metavar='<instance-uuid>',
           help='ID of instance.')
def do_detach(cs, args):
    """Clear attachment metadata."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.detach(volume.id, args.instance_uuid)
        print ("Request to detach volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to detach volume %s failed: %s." % (
            volume.id, e))


@utils.arg('volume',
           metavar='<volume>', nargs='+',
           help='ID or name of volume or volumes to delete.')
def do_delete(cs, args):
    """Delete error or available sg volume."""
    failure_count = 0
    for item in args.volume:
        try:
            volume = shell_utils.find_volume(cs, item)
            cs.volumes.delete(volume.id)
            print ("Request to delete volume %s has been accepted." % item)
        except Exception as e:
            failure_count += 1
            print ("Request to delete volume %s failed: %s." % (item, e))
    if failure_count == len(args.volume):
        raise exceptions.CommandError("Unable to delete any of the specified "
                                      "volumes.")


@utils.arg('volume', metavar='<volume>',
           help='ID or name of the volume to modify.')
@utils.arg('--state', metavar='<state>',
           default='available',
           help='The state to assign to the volume.')
def do_reset_state(cs, args):
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.reset_state(volume.id, args.state)
        print("Request to reset-state volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print("Reset-state for volume %s failed: %s" % (volume.id, e))

###################


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_force_failover(cs, args):
    """Force failover volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.failover(volume.id, force=True)
    utils.print_dict(volume.to_dict())

#######################


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of snapshot.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of snapshot.')
def do_snapshot_create(cs, args):
    """Create snapshot."""
    volume = shell_utils.find_volume(cs, args.volume)
    snapshot = cs.snapshots.create(volume.id, args.name, args.description)
    utils.print_dict(snapshot.to_dict())


@utils.arg('snapshot',
           metavar='<snapshot>', nargs='+',
           help='ID or name of snapshot or snapshots to delete.')
def do_snapshot_delete(cs, args):
    """Delete snapshot."""
    failure_count = 0
    for item in args.snapshot:
        try:
            snapshot = shell_utils.find_snapshot(cs, item)
            cs.snapshots.delete(snapshot.id)
            print("Request to delete snapshot %s has been accepted." % item)
        except Exception as e:
            failure_count += 1
            print("Delete for snapshot %s failed: %s" % (item, e))
    if failure_count == len(args.snapshot):
        raise exceptions.CommandError("Unable to delete any of the specified "
                                      "snapshots.")


@utils.arg('snapshot',
           metavar='<snapshot>',
           help='ID or name of snapshot.')
def do_snapshot_show(cs, args):
    """Get snapshot."""
    snapshot = shell_utils.find_snapshot(cs, args.snapshot)
    utils.print_dict(snapshot.to_dict())


@utils.arg('snapshot',
           metavar='<snapshot>',
           help='ID or name of snapshot.')
def do_snapshot_rollback(cs, args):
    """Rollback snapshot."""
    snapshot = shell_utils.find_snapshot(cs, args.snapshot)
    rollback = cs.snapshots.rollback(snapshot.id)
    utils.print_dict(rollback.to_dict())


@utils.arg('--all-tenants',
           dest='all_tenants',
           metavar='<0|1>',
           nargs='?',
           type=int,
           const=1,
           default=0,
           help='Shows details for all tenants. Admin only.')
@utils.arg('--all_tenants',
           nargs='?',
           type=int,
           const=1,
           help=argparse.SUPPRESS)
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--volume-id',
           metavar='<volume_id>',
           default=None,
           help='Filters results by a volume ID. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning plans that appear later in the plan '
                'list than that represented by this plan id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of plans to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort',
           metavar='<key>[:<direction>]',
           default=None,
           help=(('Comma-separated list of sort keys and directions in the '
                  'form of <key>[:<asc|desc>]. '
                  'Valid keys: %s. '
                  'Default=None.') % ', '.join(base.SORT_KEY_VALUES)))
@utils.arg('--tenant',
           type=str,
           dest='tenant',
           nargs='?',
           metavar='<tenant>',
           help='Display information from single tenant (Admin only).')
def do_snapshot_list(cs, args):
    """list snapshots."""
    all_tenants = 1 if args.tenant else \
        int(os.environ.get("ALL_TENANTS", args.all_tenants))
    search_opts = {
        'all_tenants': all_tenants,
        'project_id': args.tenant,
        'name': args.name,
        'status': args.status,
        'volume_id': args.volume_id
    }

    if args.sort and (args.sort_key or args.sort_dir):
        raise exceptions.CommandError(
            'The --sort_key and --sort_dir arguments are deprecated and are '
            'not supported with --sort.')

    snapshots = cs.snapshots.list(search_opts=search_opts, marker=args.marker,
                                  limit=args.limit, sort_key=args.sort_key,
                                  sort_dir=args.sort_dir, sort=args.sort)
    columns = ['Id', 'Name', 'Status', 'Volume id']

    if args.sort_key or args.sort_dir or args.sort:
        sortby_index = None
    else:
        sortby_index = 0
    utils.print_list(snapshots, columns, exclude_unavailable=True,
                     sortby_index=sortby_index)


@utils.arg('snapshot',
           metavar='<snapshot>',
           help='Name or ID of snapshot to update.')
@utils.arg('--name',
           nargs='?',
           metavar='<name>',
           help='New name for snapshot.')
@utils.arg('--description',
           nargs='?',
           metavar='<description>',
           help='New description for snapshot.')
def do_snapshot_update(cs, args):
    kwargs = {}
    if args.name is not None:
        kwargs['name'] = args.name
    if args.description is not None:
        kwargs['description'] = args.description

    if not kwargs:
        msg = 'Must supply either name or description.'
        raise exceptions.ClientException(code=1, message=msg)

    snapshot = shell_utils.find_snapshot(cs, args.snapshot)
    snapshot = cs.snapshots.update(snapshot.id, kwargs)
    utils.print_dict(snapshot.to_dict())


@utils.arg('snapshot', metavar='<snapshot>',
           help='ID or name of the snapshot to modify.')
@utils.arg('--state', metavar='<state>',
           default='available',
           help='The state to assign to the snapshot.')
def do_snapshot_reset_state(cs, args):
    snapshot = shell_utils.find_snapshot(cs, args.snapshot)
    try:
        cs.snapshots.reset_state(snapshot.id, args.state)
        print("Request to reset-state snapshot %s has been accepted." % (
            snapshot.id))
    except Exception as e:
        print("Reset-state for snapshot %s failed: %s" % (snapshot.id, e))


####################

@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of backup.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of backup.')
@utils.arg('--type',
           metavar='<type>',
           help='Full or incremental backup.')
@utils.arg('--destination',
           metavar='<destination>',
           help='Local or remote backup.')
def do_backup_create(cs, args):
    """Create backup."""
    type = args.type
    type = 'full' if type is None else type
    if type not in ['full', 'incremental']:
        print("Backup type must be full or incremental")
        return
    destination = args.destination
    destination = 'local' if destination is None else destination
    if destination not in ['local', 'remote']:
        print("Backup destination must be local or remote")
        return
    volume = shell_utils.find_volume(cs, args.volume)
    backup = cs.backups.create(volume_id=volume.id, name=args.name,
                               description=args.description,
                               type=type, destination=destination)
    utils.print_dict(backup.to_dict())


@utils.arg('backup',
           metavar='<backup>', nargs='+',
           help='ID or name of backup.')
def do_backup_delete(cs, args):
    """Delete snapshot."""
    failure_count = 0
    for item in args.backup:
        try:
            backup = shell_utils.find_backup(cs, item)
            cs.backups.delete(backup.id)
            print("Request to delete backup %s has been accepted." % item)
        except Exception as e:
            print("Delete for backup %s failed: %s" % (item, e))
    if failure_count == len(args.backup):
        raise exceptions.CommandError("Unable to delete any of the specified "
                                      "backups.")


@utils.arg('backup',
           metavar='<backup>',
           help='ID or name of backup.')
def do_backup_show(cs, args):
    """Get backup."""
    backup = shell_utils.find_backup(cs, args.backup)
    utils.print_dict(backup.to_dict())


@utils.arg('backup',
           metavar='<backup>',
           help='ID or name of backup.')
@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of restoring cinder volume.')
def do_backup_restore(cs, args):
    """Restore backup."""
    backup = shell_utils.find_backup(cs, args.backup)
    restore = cs.backups.restore(backup.id, args.volume_id)
    utils.print_dict(restore.to_dict())


@utils.arg('--all-tenants',
           dest='all_tenants',
           metavar='<0|1>',
           nargs='?',
           type=int,
           const=1,
           default=0,
           help='Shows details for all tenants. Admin only.')
@utils.arg('--all_tenants',
           nargs='?',
           type=int,
           const=1,
           help=argparse.SUPPRESS)
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--volume-id',
           metavar='<volume_id>',
           default=None,
           help='Filters results by a volume ID. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning plans that appear later in the plan '
                'list than that represented by this plan id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of plans to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort',
           metavar='<key>[:<direction>]',
           default=None,
           help=(('Comma-separated list of sort keys and directions in the '
                  'form of <key>[:<asc|desc>]. '
                  'Valid keys: %s. '
                  'Default=None.') % ', '.join(base.SORT_KEY_VALUES)))
@utils.arg('--tenant',
           type=str,
           dest='tenant',
           nargs='?',
           metavar='<tenant>',
           help='Display information from single tenant (Admin only).')
def do_backup_list(cs, args):
    """list backups."""
    all_tenants = 1 if args.tenant else \
        int(os.environ.get("ALL_TENANTS", args.all_tenants))
    search_opts = {
        'all_tenants': all_tenants,
        'project_id': args.tenant,
        'name': args.name,
        'status': args.status,
        'volume_id': args.volume_id
    }

    if args.sort and (args.sort_key or args.sort_dir):
        raise exceptions.CommandError(
            'The --sort_key and --sort_dir arguments are deprecated and are '
            'not supported with --sort.')

    backups = cs.backups.list(search_opts=search_opts, marker=args.marker,
                              limit=args.limit, sort_key=args.sort_key,
                              sort_dir=args.sort_dir, sort=args.sort)
    columns = ['Id', 'Name', 'Status', 'Volume id']

    if args.sort_key or args.sort_dir or args.sort:
        sortby_index = None
    else:
        sortby_index = 0
    utils.print_list(backups, columns, exclude_unavailable=True,
                     sortby_index=sortby_index)


@utils.arg('backup',
           metavar='<backup>',
           help='ID or name of backup.')
def do_backup_export(cs, args):
    """Export backup record."""
    backup = shell_utils.find_backup(cs, args.backup)
    backup_record = cs.backups.export_record(backup.id)
    utils.print_dict(backup_record.to_dict())


@utils.arg('backup_type',
           metavar='<backup_type>',
           help='Type of backup, full or incremental.')
@utils.arg('availability_zone',
           metavar='<availability_zone>',
           help='Availability zone of backup.')
@utils.arg('backup_size',
           metavar='<backup_size>',
           help='Size of backup.')
@utils.arg('--driver-data-json',
           type=str,
           dest='driver_data_json',
           default=None,
           help='Driver data in json format')
@utils.arg('--driver-data',
           action='append',
           metavar='key=val[,key=val,...]',
           default=[],
           help='Driver data info.')
def do_backup_import(cs, args):
    """Import a backup from record"""
    driver_data = _extract_driver_data(args)
    backup_record = {
        'availability_zone': args.availability_zone,
        'backup_type': args.backup_type,
        'backup_size': args.backup_size,
        'driver_data': driver_data
    }
    backup = cs.backups.import_record(backup_record)
    utils.print_dict(backup.to_dict())


def _extract_driver_data(args):
    if all((args.driver_data_json, args.driver_data)):
        raise exceptions.CommandError(
            "Must provider parameters "
            "driver-data-json or driver-data, not both")
    if not any((args.driver_data_json, args.driver_data)):
        return {}

    if args.driver_data_json:
        return jsonutils.loads(args.driver_data_json)
    driver_data = {}
    for resource_params in args.driver_data:
        for param_kv in resource_params.split(','):
            key, value = param_kv.split('=')
            driver_data[key] = value
    return driver_data


@utils.arg('backup',
           metavar='<backup>',
           help='Name or ID of backup to update.')
@utils.arg('--name',
           nargs='?',
           metavar='<name>',
           help='New name for backup.')
@utils.arg('--description',
           nargs='?',
           metavar='<description>',
           help='New description for backup.')
def do_backup_update(cs, args):
    kwargs = {}
    if args.name is not None:
        kwargs['name'] = args.name
    if args.description is not None:
        kwargs['description'] = args.description

    if not kwargs:
        msg = 'Must supply either name or description.'
        raise exceptions.ClientException(code=1, message=msg)

    backup = shell_utils.find_backup(cs, args.backup)
    backup = cs.backups.update(backup.id, kwargs)
    utils.print_dict(backup.to_dict())


@utils.arg('backup', metavar='<backup>',
           help='ID or name of the backup to modify.')
@utils.arg('--state', metavar='<state>',
           default='available',
           help='The state to assign to the backup.')
def do_backup_reset_state(cs, args):
    backup = shell_utils.find_backup(cs, args.backup)
    try:
        cs.backups.reset_state(backup.id, args.state)
        print("Request to reset-state backup %s has been accepted." % (
            backup.id))
    except Exception as e:
        print("Reset-state for backup %s failed: %s" % (backup.id, e))


#############################
@utils.arg('replication',
           metavar='<replication>',
           help='ID or name of checkpoint.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of checkpoint.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of checkpoint.')
def do_checkpoint_create(cs, args):
    """Create checkpoint."""
    replication = shell_utils.find_replication(cs, args.replication)
    checkpoint = cs.checkpoints.create(replication.id, args.name,
                                       args.description)
    utils.print_dict(checkpoint.to_dict())


@utils.arg('checkpoint',
           metavar='<checkpoint>', nargs='+',
           help='ID or name of checkpoint.')
def do_checkpoint_delete(cs, args):
    """Delete checkpoint."""
    failure_count = 0
    for item in args.checkpoint:
        try:
            checkpoint = shell_utils.find_checkpoint(cs, item)
            cs.checkpoints.delete(checkpoint.id)
            print("Request to delete checkpoint %s has been accepted." % item)
        except Exception as e:
            print("Delete for checkpoint %s failed: %s" % (item, e))
    if failure_count == len(args.checkpoint):
        raise exceptions.CommandError("Unable to delete any of the specified "
                                      "checkpoints.")


@utils.arg('checkpoint',
           metavar='<checkpoint>',
           help='ID or name of checkpoint.')
def do_checkpoint_show(cs, args):
    """Get checkpoint."""
    checkpoint = shell_utils.find_checkpoint(cs, args.checkpoint)
    utils.print_dict(checkpoint.to_dict())


@utils.arg('checkpoint',
           metavar='<checkpoint>',
           help='ID or name of checkpoint.')
def do_checkpoint_rollback(cs, args):
    """Rollback checkpoint."""
    checkpoint = shell_utils.find_checkpoint(cs, args.checkpoint)
    rollback = cs.checkpoints.rollback(checkpoint.id)
    utils.print_dict(rollback.to_dict())


@utils.arg('--all-tenants',
           dest='all_tenants',
           metavar='<0|1>',
           nargs='?',
           type=int,
           const=1,
           default=0,
           help='Shows details for all tenants. Admin only.')
@utils.arg('--all_tenants',
           nargs='?',
           type=int,
           const=1,
           help=argparse.SUPPRESS)
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--replication-id',
           metavar='<replication_id>',
           default=None,
           help='Filters results by a replication ID. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning plans that appear later in the plan '
                'list than that represented by this plan id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of plans to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort',
           metavar='<key>[:<direction>]',
           default=None,
           help=(('Comma-separated list of sort keys and directions in the '
                  'form of <key>[:<asc|desc>]. '
                  'Valid keys: %s. '
                  'Default=None.') % ', '.join(base.SORT_KEY_VALUES)))
@utils.arg('--tenant',
           type=str,
           dest='tenant',
           nargs='?',
           metavar='<tenant>',
           help='Display information from single tenant (Admin only).')
def do_checkpoint_list(cs, args):
    """list checkpoints."""
    all_tenants = 1 if args.tenant else \
        int(os.environ.get("ALL_TENANTS", args.all_tenants))
    search_opts = {
        'all_tenants': all_tenants,
        'project_id': args.tenant,
        'name': args.name,
        'status': args.status,
        'replication_id': args.replication_id
    }

    if args.sort and (args.sort_key or args.sort_dir):
        raise exceptions.CommandError(
            'The --sort_key and --sort_dir arguments are deprecated and are '
            'not supported with --sort.')

    checkpoints = cs.checkpoints.list(search_opts=search_opts,
                                      marker=args.marker,
                                      limit=args.limit, sort_key=args.sort_key,
                                      sort_dir=args.sort_dir, sort=args.sort)
    columns = ['Id', 'Name', 'Status', 'Replication id']

    if args.sort_key or args.sort_dir or args.sort:
        sortby_index = None
    else:
        sortby_index = 0
    utils.print_list(checkpoints, columns, exclude_unavailable=True,
                     sortby_index=sortby_index)


@utils.arg('checkpoint', metavar='<checkpoint>',
           help='ID or name of the checkpoint to modify.')
@utils.arg('--state', metavar='<state>',
           default='available',
           help='The state to assign to the checkpoint.')
def do_checkpoint_reset_state(cs, args):
    checkpoint = shell_utils.find_checkpoint(cs, args.checkpoint)
    try:
        cs.checkpoints.reset_state(checkpoint.id, args.state)
        print("Request to reset-state checkpoint %s has been accepted." % (
            checkpoint.id))
    except Exception as e:
        print("Reset-state for checkpoint %s failed: %s" % (checkpoint.id, e))


@utils.arg('checkpoint',
           metavar='<checkpoint>',
           help='Name or ID of checkpoint to update.')
@utils.arg('--name',
           nargs='?',
           metavar='<name>',
           help='New name for checkpoint.')
@utils.arg('--description',
           nargs='?',
           metavar='<description>',
           help='New description for checkpoint.')
def do_checkpoint_update(cs, args):
    kwargs = {}
    if args.name is not None:
        kwargs['name'] = args.name
    if args.description is not None:
        kwargs['description'] = args.description

    if not kwargs:
        msg = 'Must supply either name or description.'
        raise exceptions.ClientException(code=1, message=msg)

    checkpoint = shell_utils.find_checkpoint(cs, args.checkpoint)
    checkpoint = cs.checkpoints.update(checkpoint.id, kwargs)
    utils.print_dict(checkpoint.to_dict())
