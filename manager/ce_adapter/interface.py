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

__all__ = ("Interface", "ContainerState", "CEAdapterError", "EngineAPIError", "NotFound")


import abc
import typing


class CEAdapterError(Exception):
    pass


class EngineAPIError(CEAdapterError):
    pass


class NotFound(CEAdapterError):
    pass


class ContainerState:
    running = "active"
    stopped = "inactive"


class Interface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def listContainers(self) -> dict:
        pass

    @abc.abstractmethod
    def startContainer(self, name: str) -> None:
        pass

    @abc.abstractmethod
    def stopContainer(self, name: str) -> None:
        pass

    @abc.abstractmethod
    def createContainer(self, name: str, dpy_conf: dict, srv_conf: typing.Optional[dict] = None, env_conf: typing.Optional[dict] = None) -> None:
        pass

    @abc.abstractmethod
    def removeContainer(self, name: str, purge: bool = False) -> None:
        pass
