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

from sgsclient.common import utils


#################

@utils.arg('--name',
           metavar='<name>',
           help='Replication name.')
@utils.arg('master_volume',
           metavar='<master-volume>',
           help='ID of master-volume.')
@utils.arg('slave_volume',
           metavar='<slave-volume>',
           help='ID of slave-volume.')
@utils.arg('--description',
           metavar='<description>',
           help='The description of a replication.')
def do_replication_create(cs, args):
    """Create a replication."""
    replication = cs.replications.create(
        args.name, args.master_volume, args.slave_volume, args.description)
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


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_show(cs, args):
    """Get a replication."""
    replication = cs.replications.get(args.replication_id)
    utils.print_dict(replication.to_dict())


################

@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_get(cs, args):
    """Get a volume."""
    volume = cs.volumes.get(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_enable_sg(cs, args):
    """Enable volume's SG."""
    volume = cs.volumes.enable(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_disable_sg(cs, args):
    """Disable volume's SG."""
    volume = cs.volumes.disable(args.volume_id)
    utils.print_dict(volume.to_dict())


# TODO(luobin): remove these following volume-actions from shell
@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('instance_uuid',
           metavar='<instance-id>',
           help='ID of instance.')
def do_attach(cs, args):
    """Add sg-volume attachment metadata."""
    cs.volumes.attach(args.volume_id, args.instance_uuid, "/dev/sdb")


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_reserve(cs, args):
    """Mark SG-volume as reserved before attach."""
    cs.volumes.reserve(args.volume_id)


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_unreserve(cs, args):
    """Unmark SG-volume as reserved before attach."""
    cs.volumes.unreserve(args.volume_id)


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_initialize_connection(cs, args):
    """Initialize volume attachment."""
    connection_info = cs.volumes.initialize_connection(args.volume_id)
    utils.print_dict(connection_info.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_detach(cs, args):
    """Clear attachment metadata."""
    cs.volumes.detach(args.volume_id)


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_begin_detaching(cs, args):
    """Update volume status to 'detaching'."""
    cs.volumes.begin_detaching(args.volume_id)


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_roll_detaching(cs, args):
    """Roll back volume status to 'in-use'."""
    cs.volumes.roll_detaching(args.volume_id)


###################

# TODO(luobin): remove replicate-actions from shell
@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('peer_volume',
           metavar='<peer-volume>',
           help='ID of peer-volume.')
@utils.arg('--mode',
           metavar='<mode>',
           default='master',
           help='ID of volume.')
def do_replicate_create(cs, args):
    """Create volume's replicate."""
    volume = cs.replicates.create(args.volume_id, args.mode, args.peer_volume)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_replicate_enable(cs, args):
    """Enable volume's replicate."""
    volume = cs.replicates.enable(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_replicate_disable(cs, args):
    """Disable volume's replicate."""
    volume = cs.replicates.disable(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_replicate_delete(cs, args):
    """Delete volume's replicate."""
    volume = args.volume_id
    try:
        cs.replicates.delete(args.volume_id)
        print("Request to delete volume %s replicate has been accepted." % (
            volume))
    except Exception as e:
        print("Delete for volume %s replicate failed: %s" % (volume, e))


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_replicate_failover(cs, args):
    """Failover volume's replicate."""
    volume = cs.replicates.failover(args.volume_id)
    utils.print_dict(volume.to_dict())


@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
def do_replicate_reverse(cs, args):
    """Reverse volume's replicate."""
    volume = cs.replicates.reverse(args.volume_id)
    utils.print_dict(volume.to_dict())


#######################

@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of snapshot.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of snapshot.')
def do_snapshot_create(cs, args):
    """Create snapshot."""
    snapshot = cs.snapshots.create(args.volume_id, args.name, args.description)
    utils.print_dict(snapshot.to_dict())


@utils.arg('snapshot_id',
           metavar='<snapshot-id>',
           help='ID of snapshot.')
def do_snapshot_delete(cs, args):
    """Delete snapshot."""
    snapshot = args.snapshot_id
    try:
        cs.snapshots.delete(snapshot)
        print("Request to delete snapshot %s has been accepted." % (
            snapshot))
    except Exception as e:
        print("Delete for snapshot %s failed: %s" % (snapshot, e))


@utils.arg('snapshot_id',
           metavar='<snapshot-id>',
           help='ID of snapshot.')
def do_snapshot_show(cs, args):
    """Get snapshot."""
    snapshot = cs.snapshots.get(args.snapshot_id)
    utils.print_dict(snapshot.to_dict())


####################

@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of volume.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of backup.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of backup.')
def do_backup_create(cs, args):
    """Create backup."""
    backup = cs.backups.create(args.volume_id, args.name, args.description)
    utils.print_dict(backup.to_dict())


@utils.arg('backup_id',
           metavar='<backup-id>',
           help='ID of backup.')
def do_backup_delete(cs, args):
    """Delete snapshot."""
    backup = args.backup_id
    try:
        cs.backups.delete(backup)
        print("Request to delete backup %s has been accepted." % (
            backup))
    except Exception as e:
        print("Delete for backup %s failed: %s" % (backup, e))


@utils.arg('backup_id',
           metavar='<backup-id>',
           help='ID of backup.')
def do_backup_show(cs, args):
    """Get backup."""
    backup = cs.backups.get(args.backup_id)
    utils.print_dict(backup.to_dict())


@utils.arg('backup_id',
           metavar='<backup-id>',
           help='ID of backup.')
@utils.arg('volume_id',
           metavar='<volume-id>',
           help='ID of restoring volume.')
def do_backup_restore(cs, args):
    """Restore backup."""
    backup = cs.backups.restore(args.backup_id, args.volume_id)
    utils.print_dict(backup.to_dict())
