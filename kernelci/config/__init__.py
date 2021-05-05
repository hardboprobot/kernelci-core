# Copyright (C) 2021 Collabora Limited
# Author: Guillaume Tucker <guillaume.tucker@collabora.com>
#
# This module is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import glob
import os
import yaml

import kernelci.config
import kernelci.config.build
import kernelci.config.data
import kernelci.config.lab
import kernelci.config.rootfs
import kernelci.config.test


def load_yaml(config_path, verbose=False):
    yaml_files = glob.glob(os.path.join(config_path, "*.yaml"))
    config = dict()
    for yaml_path in yaml_files:
        if verbose:
            print("Loading {}".format(yaml_path))
        with open(yaml_path) as yaml_file:
            data = yaml.safe_load(yaml_file)
            for k, v in data.items():
                config_value = config.setdefault(k, v.__class__())
                if hasattr(config_value, 'update'):
                    config_value.update(v)
                elif hasattr(config_value, 'extend'):
                    config_value.extend(v)
                else:
                    config[k] = v
    return config


def load_config(data):
    config = dict()
    config.update(kernelci.config.build.from_yaml(data))
    config.update(kernelci.config.data.from_yaml(data))
    config.update(kernelci.config.lab.from_yaml(data))
    config.update(kernelci.config.rootfs.from_yaml(data))
    config.update(kernelci.config.test.from_yaml(data))
    return config


def load(config_path, verbose=False):
    data = load_yaml(config_path)
    return load_config(data)
