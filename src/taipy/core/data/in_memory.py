# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from taipy.config.common.scope import Scope

from .._version._version_manager_factory import _VersionManagerFactory
from ..common.alias import DataNodeId, Edit
from .data_node import DataNode

in_memory_storage: Dict[str, Any] = {}


class InMemoryDataNode(DataNode):
    """Data Node stored in memory.

    Warning:
        This Data Node implementation is not compatible with a parallel execution of taipy tasks,
        but only with a task executor in development mode. The purpose of `InMemoryDataNode` is to be used
        for development or debugging.

    Attributes:
        config_id (str): Identifier of the data node configuration. It must be a valid Python
            identifier.
        scope (Scope^): The scope of this data node.
        id (str): The unique identifier of this data node.
        name (str): A user-readable name of this data node.
        owner_id (str): The identifier of the owner (pipeline_id, scenario_id, cycle_id) or
            `None`.
        parent_ids (Optional[Set[str]]): The identifiers of the parent tasks or `None`.
        last_edit_date (datetime): The date and time of the last modification.
        edits (List[Edit^]): The ordered list of edits for that job.
        version (str): The string indicates the application version of the data node to instantiate. If not provided,
            the current version is used.
        validity_period (Optional[timedelta]): The validity period of a data node.
            Implemented as a timedelta. If _validity_period_ is set to None, the data_node is
            always up-to-date.
        edit_in_progress (bool): True if a task computing the data node has been submitted
            and not completed yet. False otherwise.
        properties (dict[str, Any]): A dictionary of additional properties. When creating an
            _In Memory_ data node, if the _properties_ dictionary contains a _"default_data"_
            entry, the data node is automatically written with the corresponding _"default_data"_
            value.
    """

    __STORAGE_TYPE = "in_memory"
    __DEFAULT_DATA_VALUE = "default_data"
    _REQUIRED_PROPERTIES: List[str] = []

    def __init__(
        self,
        config_id: str,
        scope: Scope,
        id: Optional[DataNodeId] = None,
        name: Optional[str] = None,
        owner_id: Optional[str] = None,
        parent_ids: Optional[Set[str]] = None,
        last_edit_date: Optional[datetime] = None,
        edits: List[Edit] = None,
        version: str = None,
        validity_period: Optional[timedelta] = None,
        edit_in_progress: bool = False,
        properties=None,
    ):
        if properties is None:
            properties = {}
        default_value = properties.pop(self.__DEFAULT_DATA_VALUE, None)
        super().__init__(
            config_id,
            scope,
            id,
            name,
            owner_id,
            parent_ids,
            last_edit_date,
            edits,
            version or _VersionManagerFactory._build_manager()._get_latest_version(),
            validity_period,
            edit_in_progress,
            **properties
        )
        if default_value is not None and self.id not in in_memory_storage:
            self.write(default_value)

    @classmethod
    def storage_type(cls) -> str:
        return cls.__STORAGE_TYPE

    def _read(self):
        return in_memory_storage.get(self.id)

    def _write(self, data):
        in_memory_storage[self.id] = data

    @classmethod
    def _serialize_datanode_properties(cls, datanode_properties: dict) -> dict:
        return datanode_properties

    @classmethod
    def _deserialize_datanode_model_properties(cls, datanode_model_properties: dict) -> dict:
        return datanode_model_properties
