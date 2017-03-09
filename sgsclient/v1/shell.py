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


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_enable(cs, args):
    """Enable a replication."""
    replication = cs.replications.enable(args.replication_id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_disable(cs, args):
    """Disable a replication."""
    replication = cs.replications.disable(args.replication_id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_failover(cs, args):
    """Failover a replication."""
    replication = cs.replications.failover(args.replication_id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_reverse(cs, args):
    """Reverse a replication."""
    replication = cs.replications.reverse(args.replication_id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_delete(cs, args):
    """Delete a replication."""
    replication = args.replication_id
    try:
        cs.replications.delete(replication)
        print("Request to delete replication %s has been accepted." % (
            replication))
    except Exception as e:
        print("Delete for replication %s failed: %s" % (replication, e))


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
    columns = ['Id', 'Name', 'Status', 'Replicate Status']

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
@utils.arg('--volume_type',
           metavar='<volume-type>',
           help='Volume type.')
@utils.arg('--availability_zone',
           metavar='<availability-zone>',
           help='availability zone')
def do_create_volume(cs, args):
    """Create a volume."""
    try:
        cs.volumes.create(checkpoint_id=args.checkpoint_id,
                          snapshot_id=args.snapshot_id,
                          name=args.name,
                          description=args.description,
                          volume_type=args.volume_type,
                          availability_zone=args.availability_zone)
        print("Request to create volume has been accepted.")
    except Exception as e:
        print("Create volume request failed: %s" % e)


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Replication name.')
@utils.arg('--description',
           metavar='<description>',
           help='The description of a replication.')
def do_enable_sg(cs, args):
    """Enable volume's SG."""
    volume = cs.volumes.enable(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_disable_sg(cs, args):
    """Disable volume's SG."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.volumes.disable(volume.id)
    utils.print_dict(volume.to_dict())


# TODO(luobin): remove these following volume-actions from shell
@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('--instance_uuid',
           metavar='<instance-id>',
           help='ID of instance.')
@utils.arg('--host_name',
           metavar='<host-name>',
           help='The name of host.')
@utils.arg('--mountpoint',
           metavar='<mountpoint>',
           help='The mountpoint.')
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
    try:
        cs.volumes.attach(volume.id, args.instance_uuid, args.mountpoint,
                          args.mode, args.host_name)
        print ("Request to attach volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to attach volume %s failed: %s." % (
            volume.id, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_reserve(cs, args):
    """Mark SG-volume as reserved before attach."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.reserve(volume.id)
        print ("Request to reserve volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to reserve volume %s failed: %s." % (
            volume.id, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_unreserve(cs, args):
    """Unmark SG-volume as reserved before attach."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.unreserve(volume.id)
        print ("Request to unreserve volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to unreserve volume %s failed: %s." % (volume.id, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_initialize_connection(cs, args):
    """Initialize volume attachment."""
    volume = shell_utils.find_volume(cs, args.volume)
    connection_info = cs.volumes.initialize_connection(volume.id)
    utils.print_dict(connection_info.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_detach(cs, args):
    """Clear attachment metadata."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.detach(volume.id)
        print ("Request to detach volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to detach volume %s failed: %s." % (
            volume.id, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_begin_detaching(cs, args):
    """Update volume status to 'detaching'."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.begin_detaching(volume.id)
        print ("Request to begin_detaching %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to begin_detaching %s failed: %s." % (
            volume.id, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_roll_detaching(cs, args):
    """Roll back volume status to 'in-use'."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.volumes.roll_detaching(volume.id)
        print ("Request to roll_detaching volume %s has been accepted." % (
            volume.id))
    except Exception as e:
        print ("Request to roll_detaching volume %s failed: %s." % (
            volume.id, e))


###################

# TODO(luobin): remove replicate-actions from shell
@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
@utils.arg('peer_volume',
           metavar='<peer-volume>',
           help='ID of peer-volume.')
@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
@utils.arg('--mode',
           metavar='<mode>',
           default='master',
           help='ID of volume.')
def do_replicate_create(cs, args):
    """Create volume's replicate."""
    mode = args.mode
    mode = 'master' if mode is None else mode
    if mode not in ['master', 'slave']:
        print("Replicate mode must be master or slave")
        return
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.create(volume_id=volume.id, mode=mode,
                                  replication_id=args.replication_id,
                                  peer_volume=args.peer_volume)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_enable(cs, args):
    """Enable volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.enable(volume.id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_disable(cs, args):
    """Disable volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.disable(volume.id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_delete(cs, args):
    """Delete volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    try:
        cs.replicates.delete(volume.id)
        print("Request to delete volume %s replicate has been accepted." % (
            volume))
    except Exception as e:
        print("Delete for volume %s replicate failed: %s" % (volume, e))


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_failover(cs, args):
    """Failover volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.failover(volume.id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume',
           metavar='<volume>',
           help='ID or name of volume.')
def do_replicate_reverse(cs, args):
    """Reverse volume's replicate."""
    volume = shell_utils.find_volume(cs, args.volume)
    volume = cs.replicates.reverse(volume.id)
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
           metavar='<snapshot>',
           help='ID or name of snapshot.')
def do_snapshot_delete(cs, args):
    """Delete snapshot."""
    snapshot = shell_utils.find_snapshot(cs, args.snapshot)
    try:
        cs.snapshots.delete(snapshot.id)
        print("Request to delete snapshot %s has been accepted." % (
            snapshot.id))
    except Exception as e:
        print("Delete for snapshot %s failed: %s" % (snapshot.id, e))


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
           metavar='<backup>',
           help='ID or name of backup.')
def do_backup_delete(cs, args):
    """Delete snapshot."""
    backup = shell_utils.find_backup(cs, args.backup)
    try:
        cs.backups.delete(backup.id)
        print("Request to delete backup %s has been accepted." % (
            backup.id))
    except Exception as e:
        print("Delete for backup %s failed: %s" % (backup.id, e))


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
           metavar='<checkpoint>',
           help='ID or name of checkpoint.')
def do_checkpoint_delete(cs, args):
    """Delete checkpoint."""
    checkpoint = shell_utils.find_checkpoint(cs, args.checkpoint)
    try:
        cs.checkpoints.delete(checkpoint.id)
        print("Request to delete checkpoint %s has been accepted." % (
            checkpoint.id))
    except Exception as e:
        print("Delete for checkpoint %s failed: %s" % (checkpoint.id, e))


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
