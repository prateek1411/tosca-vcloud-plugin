# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup

setup(
    zip_safe=True,
    name='cloudify-vcloud-plugin',
    version='1.4',
    packages=[
        'vcloud_plugin_common',
        'vcloud_server_plugin',
        'vcloud_storage_plugin',
        'vcloud_network_plugin'
    ],
    license='LICENSE',
    description='Cloudify plugin for vmWare vCloud infrastructure.',
    dependency_links = ['https://github.com/cloudify-cosmo/pyvcloud/tarball/isolated_net#egg=pyvcloud-16.1.0'],
    install_requires=[
        'cloudify-plugins-common>=3.4',
        'requests==2.7.0',
        'IPy==0.81',
        'PyYAML==3.10',
        'pycrypto==2.6.1',
        'pyvcloud==16.1.0'
    ]
)
