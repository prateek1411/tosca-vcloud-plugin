# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.

from cloudify import ctx
from cloudify.decorators import operation
from cloudify import exceptions as cfy_exc

from vcloud_plugin_common import (transform_resource_name,
                                  wait_for_task,
                                  with_vcd_client)

VCLOUD_VAPP_NAME = 'vcloud_vapp_name'
STATUS_POWER_ON = 'Powered on'
STATUS_POWER_OFF = 'Power off'

@operation
@with_vcd_client
def create(vcd_client, **kwargs):
    server = {
        'name': ctx.instance.id,
    }
    server.update(ctx.node.properties['server'])
    transform_resource_name(server, ctx)
    required_params = ('catalog', 'template')
    missed_params = set(required_params) - set(server.keys())
    if len(missed_params) > 0:
        raise cfy_exc.NonRecoverableError(
            "{0} server properties must be specified"
            .format(list(missed_params)))
    create_args = {
        '--deploy': True,
        '--on': True,
        '--blocking': False,
        '--network': None
        }
    ctx.logger.info("Creating VApp with parameters: {0}".format(str(server)))
    success, result = vcd_client.create_vApp(server['name'],
                                             server['template'],
                                             server['catalog'],
                                             create_args)

    if success is False:
        raise cfy_exc.NonRecoverableError(
            "Could not create vApp: {0}".format(result))

    task = result.get_Tasks().get_Task()[0]
    wait_for_task(vcd_client, task)
    ctx.instance.runtime_properties[VCLOUD_VAPP_NAME] = server['name']


@operation
@with_vcd_client
def start(vcd_client, **kwargs):
    vapp_name = ctx.instance.runtime_properties[VCLOUD_VAPP_NAME]
    vapp = vcd_client.get_vApp(vapp_name)
    if _vm_is_on(vapp) is False:
        ctx.logger.info("Power-on VApp {0}".format(vapp_name))
        vapp.poweron({'--blocking': True, '--json': True})


@operation
@with_vcd_client
def stop(vcd_client, **kwargs):
    vapp_name = ctx.instance.runtime_properties[VCLOUD_VAPP_NAME]
    vapp = vcd_client.get_vApp(vapp_name)
    ctx.logger.info("Power-off and undeploy VApp {0}".format(vapp_name))
    vapp.undeploy({'--blocking': True, '--json': True, '--action': 'powerOff'})


@operation
@with_vcd_client
def delete(vcd_client, **kwargs):
    vapp_name = ctx.instance.runtime_properties[VCLOUD_VAPP_NAME]
    vapp = vcd_client.get_vApp(vapp_name)
    ctx.logger.info("Deleting VApp {0}".format(vapp_name))
    vapp.delete({'--blocking': True, '--json': True})
    del ctx.instance.runtime_properties[VCLOUD_VAPP_NAME]


@operation
@with_vcd_client
def get_state(vcd_client, **kwargs):
    pass


def _vm_is_on(vapp):
    return vapp.details_of_vms()[0][1] == STATUS_POWER_ON
