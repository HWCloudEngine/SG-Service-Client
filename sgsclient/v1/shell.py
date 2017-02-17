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


@utils.arg('--checkpoint_id',
           metavar='<checkpoint-id>',
           help='ID of checkpoint.')
@utils.arg('--snapshot_id',
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
def do_create(cs, args):
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
    cs.volumes.attach(args.volume_id, args.instance_uuid, args.mountpoint,
                      args.mode, args.host_name)


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
    volume = cs.replicates.create(vollume_id=args.volume_id, mode=mode,
                                  replication_id=args.replication_id,
                                  peer_volume=args.peer_volume)
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


@utils.arg('snapshot_id',
           metavar='<snapshot-id>',
           help='ID of snapshot.')
def do_snapshot_rollback(cs, args):
    """Rollback snapshot."""
    rollback = cs.snapshots.rollback(args.snapshot_id)
    utils.print_dict(rollback.to_dict())


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
    backup = cs.backups.create(volume_id=args.volume_id, name=args.name,
                               description=args.description,
                               type=type, destination=destination)
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


#############################


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of checkpoint.')
@utils.arg('--name',
           metavar='<name>',
           help='Name of checkpoint.')
@utils.arg('--description',
           metavar='<description>',
           help='Description of checkpoint.')
def do_checkpoint_create(cs, args):
    """Create checkpoint."""
    checkpoint = cs.checkpoints.create(args.volume_id, args.name,
                                       args.description)
    utils.print_dict(checkpoint.to_dict())


@utils.arg('checkpoint_id',
           metavar='<checkpoint-id>',
           help='ID of checkpoint.')
def do_checkpoint_delete(cs, args):
    """Delete checkpoint."""
    checkpoint = args.checkpoint_id
    try:
        cs.checkpoints.delete(checkpoint)
        print("Request to delete checkpoint %s has been accepted." % (
            checkpoint))
    except Exception as e:
        print("Delete for checkpoint %s failed: %s" % (checkpoint, e))


@utils.arg('checkpoint_id',
           metavar='<checkpoint-id>',
           help='ID of checkpoint.')
def do_checkpoint_show(cs, args):
    """Get checkpoint."""
    checkpoint = cs.checkpoints.get(args.checkpoint_id)
    utils.print_dict(checkpoint.to_dict())


@utils.arg('checkpoint_id',
           metavar='<checkpoint-id>',
           help='ID of checkpoint.')
def do_checkpoint_rollback(cs, args):
    """Rollback checkpoint."""
    rollback = cs.checkpoints.rollback(args.checkpoint_id)
    utils.print_dict(rollback.to_dict())
