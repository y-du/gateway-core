"""
   Copyright 2020 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("gc_conf",)


import simple_conf
import logging
import os


formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: [%(name)s] %(message)s', datefmt='%m.%d.%Y %I:%M:%S %p')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

sc_logger = logging.getLogger('simple-conf')
sc_logger.addHandler(stream_handler)
sc_logger.setLevel(logging.WARNING)


@simple_conf.configuration
class GCConf:

    @simple_conf.section
    class CE:
        socket = "unix://var/run/docker.sock"
        network_name = "gateway-network"
        subnet = "10.20.0.0/16",
        ip_range = "10.20.0.0/24",
        gateway = "10.20.0.1"

    @simple_conf.section
    class CR:
        scheme = "http"
        host = None
        api = "components"
        cc_id = None

    @simple_conf.section
    class GCM:
        initiated = False
        whitelist = None

    @simple_conf.section
    class Logger:
        level = 'info'
        rotating_log = False
        rotating_log_backup_count = 14


user_dir = '{}/storage'.format(os.getcwd())

if not os.path.exists(user_dir):
    os.makedirs(user_dir)

gc_conf = GCConf("gc", user_dir, ext_aft_crt=False)
