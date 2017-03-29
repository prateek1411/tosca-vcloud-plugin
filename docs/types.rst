.. highlight:: yaml

Types
=====

Node Types
----------

.. _vcloud_config:

vCloud Config
^^^^^^^^^^^^^
The vCloud plugin requires credentials in order to authenticate and interact with vCloud.

This information will be gathered by the plugin from the following sources,
each source possibly partially or completely overriding values gathered from previous ones:

  1. JSON file at ``~/vcloud_config.json`` or at a path specified by the value of an environment variable named ``VCLOUD_CONFIG_PATH``
  2. values specified in the ``vcloud_config`` property for the node whose operation is currently getting executed (in the case of relationship operations,
     the ``vcloud_config`` property of either the *source* or *target* nodes will be used if available,
     with the *source*'s one taking precedence).

The structure of the JSON file in section (1), as well as of the ``vcloud_config`` property in section (2), is as follows::

    {
        "username": "",
        "password": "",
        "url": "",
        "org": "",
        "vdc": "",
        "service": "",
        "service_type": "",
        "api_version": "",
        "instance": "",
        "org_url": "",
        "ssl_verify": ""
    }

* ``username`` vCloud account username.
* ``password`` vCloud account password.
* ``url`` vCloud url.
* ``org`` Organization name. Required only for ``ondemand`` and ``subscription`` service types.
* ``instance`` Instance uuid. Required only for ``ondemand`` service type.
* ``vdc`` Virtual Datacenter name.
* ``service`` vCloud Service name.
* ``service_type`` service type. Can be ``subscription``, ``ondemand``, ``vcd`` or ``private``. ``Private`` is alias for ``vcd`` and both of this types can be used with private vcloud environment without any differences. Defaults to ``subscription``.
* ``api_version`` vCloud API version. For Subscription defaults to ``5.6``, for OnDemand - to ``5.7``.
* ``region`` region name. Applies for OnDemand.
* ``org_url`` organization url. Required only for ``private`` service type.
* ``edge_gateway`` edge gateway name.
* ``ssl_verify`` boolean flag for disable ssl certificate checks, have sense only for ``private`` cloud service with selfsigned certificates. Defaults to ``True``


.. tip::
    The vCloud manager blueprint stores the vCloud configuration used for the bootstrap process in a JSON file as described in (1) at ``~/vcloud_config.json``. Therefore, if they've been used for bootstrap, the vCloud configuration for applications isn't mandatory as the plugin will default to these same settings.


Each type has property ``vcloud_config``.
It can be used to pass parameters for authenticating.
Overriding of this property is not required,
and if running on a Cloudify Manager,
by default the authentication will take place
with the same credentials that were used for the Cloudify bootstrap process.


.. cfy:node:: cloudify.vcloud.nodes.Server


**Attributes:**

  * ``vcloud_vapp_name`` created VApp name

Two additional runtime-properties are available on node instances of this type once the ``cloudify.interfaces.host.get_state`` operation succeeds:

  * ``networks`` server networks information.
  * ``ip`` the private IP (ip on the internal network) of the server.


.. cfy:node:: cloudify.vcloud.nodes.Network

**Attributes:**

  * ``vcloud_network_name`` network name


.. cfy:node:: cloudify.vcloud.nodes.Port


.. cfy:node:: cloudify.vcloud.nodes.FloatingIP

**Attributes:**

  * ``public_ip`` public ip address


.. cfy:node:: cloudify.vcloud.nodes.PublicNAT

**Attributes:**

  * ``public_ip`` public ip address


.. cfy:node:: cloudify.vcloud.nodes.KeyPair
.. cfy:node:: cloudify.vcloud.nodes.SecurityGroup
.. cfy:node:: cloudify.vcloud.nodes.Volume
.. cfy:node:: cloudify.vcloud.nodes.VDC


Relationships
-------------

.. cfy:rel:: cloudify.vcloud.server_connected_to_floating_ip

    A relationship for associating FloatingIP node with Server node.


.. cfy:rel:: cloudify.vcloud.server_connected_to_port

    A relationship for connecting Server to Port.

.. note:: This relationship has no operations associated with it;
   The server will use this relationship to connect to the port upon server creation.


.. cfy:rel:: cloudify.vcloud.port_connected_to_network

    A relationship for connecting Port to Network.
.. note:: This relationship has no operations associated with it.


.. cfy:rel:: cloudify.vcloud.server_connected_to_network

    A relationship for connecting Server to Network.
.. note:: This relationship has no operations associated with it;
   The server will use this relationship to connect to the network upon server creation.
   It will use DHCP for ip allocation.


.. cfy:rel:: cloudify.vcloud.server_connected_to_public_nat

    A relationship for associating PublicNAT and Server.


.. cfy:rel:: cloudify.vcloud.server_connected_to_security_group

    A relationship for associating SecurityGroup and Server.


.. cfy:rel:: cloudify.vcloud.net_connected_to_public_nat

    A relationship for associating PublicNAT and Network.


.. cfy:rel:: cloudify.vcloud.server_connected_to_vdc

.. cfy:rel:: cloudify.vcloud.volume_attached_to_server
.. cfy:rel:: cloudify.vcloud.server_connected_to_keypair
.. cfy:rel:: cloudify.vcloud.delete_public_key_from_server

