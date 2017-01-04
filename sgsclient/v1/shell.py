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
    replication = cs.replications.delete(args.replication_id)
    utils.print_dict(replication.to_dict())


@utils.arg('replication_id',
           metavar='<replication-id>',
           help='ID of replication.')
def do_replication_get(cs, args):
    """Get a replication."""
    replication = cs.replications.get(args.replication_id)
    utils.print_dict(replication.to_dict())
