import os
import shutil
import uuid

import pytest
from dotenv import load_dotenv
from taipy.common.alias import DataSourceId
from taipy.config import Config, DataSourceConfig, PipelineConfig
from taipy.data import InMemoryDataSource, Scope
from taipy.pipeline import Pipeline
from taipy.scenario import Scenario
from taipy.task import Task

from taipy_rest.app import create_app


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def datasource_data():
    return {
        "name": "foo",
        "storage_type": "in_memory",
        "scope": "pipeline",
        "default_data": ["1991-01-01T00:00:00"],
    }


@pytest.fixture
def task_data():
    return {
        "config_name": "foo",
        "input_ids": ["DATASOURCE_foo_3b888e17-1974-4a56-a42c-c7c96bc9cd54"],
        "function_name": "print",
        "function_module": "builtins",
        "output_ids": ["DATASOURCE_foo_4d9923b8-eb9f-4f3c-8055-3a1ce8bee309"],
    }


@pytest.fixture
def pipeline_data():
    return {
        "name": "foo",
        "task_ids": ["TASK_foo_3b888e17-1974-4a56-a42c-c7c96bc9cd54"],
    }


@pytest.fixture
def scenario_data():
    return {
        "name": "foo",
        "pipeline_ids": ["PIPELINE_foo_3b888e17-1974-4a56-a42c-c7c96bc9cd54"],
        "properties": {},
    }


@pytest.fixture
def default_datasource():
    return InMemoryDataSource(
        "input_ds",
        Scope.SCENARIO,
        DataSourceId("id_uio"),
        "my name",
        "parent_id",
        properties={"default_data": "In memory Data Source"},
    )


@pytest.fixture
def default_datasource_config():
    return Config.add_data_source(uuid.uuid4().hex, "in_memory", Scope.PIPELINE)


@pytest.fixture
def default_datasource_config_list():
    configs = []
    for i in range(10):
        configs.append(Config.add_data_source(f"ds-{i}", "in_memory", Scope.PIPELINE))
    return configs


def __default_task():
    input_ds = InMemoryDataSource(
        "input_ds",
        Scope.SCENARIO,
        DataSourceId("id_uio"),
        "my name",
        "parent_id",
        properties={"default_data": "In memory Data Source"},
    )

    output_ds = InMemoryDataSource(
        "output_ds",
        Scope.SCENARIO,
        DataSourceId("id_uio"),
        "my name",
        "parent_id",
        properties={"default_data": "In memory Data Source"},
    )
    return Task(
        "foo",
        [input_ds],
        print,
        [output_ds],
        None,
    )


@pytest.fixture
def default_task():
    return __default_task()


def __default_pipeline():
    return Pipeline(
        config_name="foo",
        properties={},
        tasks=[__default_task()],
    )


def __task_config():
    return Config.add_task("task1", [], print, [])


@pytest.fixture
def default_pipeline():
    return __default_pipeline()


@pytest.fixture
def default_pipeline_config():
    return Config.add_pipeline(uuid.uuid4().hex, __task_config())


@pytest.fixture
def default_pipeline_config_list():
    configs = []
    for i in range(10):
        configs.append(Config.add_pipeline(uuid.uuid4().hex, __task_config()))
    return configs


@pytest.fixture
def default_scenario():
    return Scenario(
        config_name="foo",
        properties={},
        pipelines=[__default_pipeline()],
    )


@pytest.fixture(autouse=True)
def cleanup_files():
    if os.path.exists(".data"):
        shutil.rmtree(".data")
