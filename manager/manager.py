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

__all__ = ("GCManager", )


from .logger import getLogger
from .configuration import gc_conf
from .ce_adapter import DockerAdapter, CEAdapterError, ContainerState
from .util import getLocalIP
import requests
import time


logger = getLogger(__name__.split(".", 1)[-1])


def criticalExit(msg):
    logger.critical(msg)
    exit(1)


class GCManager:
    def __init__(self, ce_adapter: DockerAdapter):
        self.__ce_adapter = ce_adapter

    def initGateway(self):
        try:
            self.__ce_adapter.initNetwork()
            while True:
                response = requests.get("{}://{}/{}/{}".format(gc_conf.CR.scheme, gc_conf.CR.host, gc_conf.CR.api, gc_conf.CR.cc_id))
                if response.status_code == 200:
                    data = response.json()
                    containers = self.__ce_adapter.listContainers()
                    for name, service in data["services"].items():
                        if name not in containers:
                            logger.info("creating '{}' ...".format(name))
                            self.__ce_adapter.createContainer(
                                name,
                                service["deployment_configs"],
                                service["service_configs"],
                                {
                                    "GATEWAY_LOCAL_IP": getLocalIP(gc_conf.CR.host),
                                    "COMPONENT_ID": gc_conf.CR.cc_id
                                }
                            )
                    containers = self.__ce_adapter.listContainers()
                    for name in data["services"]:
                        if containers[name]["state"] == ContainerState.stopped:
                            logger.info("starting '{}' ...".format(name))
                            self.__ce_adapter.startContainer(name)
                    break
                logger.error("could not query component registry - {}".format(response.status_code))
                time.sleep(10)
        except KeyError as ex:
            criticalExit("initializing gateway failed - could not parse response from component registry - {}".format(ex))
        except CEAdapterError as ex:
            criticalExit("initializing gateway failed - {}".format(ex))
