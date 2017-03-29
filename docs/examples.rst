.. highlight:: yaml

Example
=======

This example will show how to use some of the types of this plugin.

The following is an excerpt from the blueprint's `blueprint`.`node_templates` section::

    example_server:
        type: cloudify.vcloud.nodes.Server
        properties:
            server:
                name: example-server
                catalog: example-catalog
                template: example-vapp-template
                hardware:
                    cpu: 2
                    memory: 4096
                guest_customization:
                    public_keys:
                        1. key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCi64cS8ZLXP9xgzscr+m7bKBDdnhTxXaarJ8hIVgG5C7FHkF1Yj9Za+JIMqGjlwsOugFt09ZTvR1kQcIXdZQhs5HWhnG8UY7RkuUwO4FOFpL2VtMAleP/ZNXSZIGwwy4Sm/wtYOo8V5GPrJNbQnVtsW2NJNt6mB1geJzlshbl9wpshHlFSOz6jV2L8k2kOq32nt/Wa3qpDk20IbKnO9wJYWHVzvyJ4bTOyHowStAABFEj8O7XmoQp8jdUuTj+qAOgCROTAQh93XbS3PJjaQYBhxLOOreYYeqjKG/8IUlFxtRdUn7MLS6Rd15AP2HnjhjKad2KqnOuFZqiTLBu+CGWf
                           user: ubuntu
                    computer_name: { get_input: manager_server_name }
            management_network: existing-network
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }
        relationships:
            1. target: example_port
               type: cloudify.vcloud.server_connected_to_port
            2. target: example_port2
               type: cloudify.vcloud.server_connected_to_port
            3. target: manager_floating_ip
               type: cloudify.vcloud.server_connected_to_floating_ip

    manager_floating_ip:
        type: cloudify.vcloud.nodes.FloatingIP
        properties:
            floatingip:
                edge_gateway: M000000000-1111
                public_ip: 24.44.244.44
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }

    example_port:
        type: cloudify.vcloud.nodes.Port
        properties:
            port:
                network: existing-network
                ip_allocation_mode: dhcp
                primary_interface: true
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }
        relationships:
            1. target: example_network
               type: cloudify.vcloud.port_connected_to_network

    example_network:
        type: cloudify.vcloud.nodes.Network
        properties:
            use_external_resource: true
            resource_id: existing-network
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }

    example_port2:
        type: cloudify.vcloud.nodes.Port
        properties:
            port:
                network: new-network
                ip_allocation_mode: manual
                ip_address: 10.10.0.2
                mac_address: 00:50:56:01:01:49
                primary_interface: false
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }
        relationships:
            1. target: example_network2
               type: cloudify.vcloud.port_connected_to_network

    example_network2:
        type: cloudify.vcloud.nodes.Network
        properties:
            network:
                edge_gateway: M000000000-1111
                name: new-network
                static_range: 10.10.0.2-10.10.0.64
                netmask: 255.255.255.0
                gateway_ip: 10.10.0.1/24
                dns: ['10.0.0.1', '8.8.8.8']
                dns_suffix: test
                dhcp:
                    dhcp_range: 10.0.0.65-10.0.0.254
                    default_lease: 3600
                    max_lease: 7200
            vcloud_config: { get_property: [vcloud_configuration, vcloud_config] }

    vcloud_configuration:
        type: vcloud_configuration
        properties:
            vcloud_config:
                username: user
                password: pw
                url: https://vchs.vmware.com
                service_type: subscription
                service: M000000000-1111
                vdc: M000000000-1111
                org: M000000000-1111
