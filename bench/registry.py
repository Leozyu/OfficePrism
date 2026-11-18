import json
from typing import Callable, Dict, Optional, Type

from loguru import logger
from pydantic import BaseModel

from bench.agent.base import BaseAgent
from bench.data_model.tasks import Task
from bench.environment.environment import Environment
from bench.user.base import BaseUser
from bench.user.user_simulator import DummyUser


class RegistryInfo(BaseModel):
    """Options for the registry"""

    domains: list[str]
    agents: list[str]
    users: list[str]
    task_sets: list[str]


class Registry:
    """Registry for Users, Agents, and Domains"""

    def __init__(self):
        self._users: Dict[str, Type[BaseUser]] = {}
        self._agents: Dict[str, Type[BaseAgent]] = {}
        self._domains: Dict[str, Callable[[], Environment]] = {}
        self._tasks: Dict[str, Callable[[], list[Task]]] = {}

    def register_user(
        self,
        user_constructor: type[BaseUser],
        name: Optional[str] = None,
    ):
        try:
            if not issubclass(user_constructor, BaseUser):
                raise TypeError(f"{user_constructor.__name__} must implement UserBase")
            key = name or user_constructor.__name__
            if key in self._users:
                raise ValueError(f"User {key} already registered")
            self._users[key] = user_constructor
        except Exception as e:
            logger.error(f"Error registering user {name}: {str(e)}")
            raise

    def register_agent(
        self,
        agent_constructor: type[BaseAgent],
        name: Optional[str] = None,
    ):
        if not issubclass(agent_constructor, BaseAgent):
            raise TypeError(f"{agent_constructor.__name__} must implement AgentBase")
        key = name or agent_constructor.__name__
        if key in self._agents:
            raise ValueError(f"Agent {key} already registered")
        self._agents[key] = agent_constructor

    def register_domain(
        self,
        get_environment: Callable[[], Environment],
        name: str,
    ):
        try:
            if name in self._domains:
                raise ValueError(f"Domain {name} already registered")
            self._domains[name] = get_environment
        except Exception as e:
            logger.error(f"Error registering domain {name}: {str(e)}")
            raise

    def register_tasks(
        self,
        get_tasks: Callable[[], list[Task]],
        name: str,
    ):
        try:
            if name in self._tasks:
                raise ValueError(f"Tasks {name} already registered")
            self._tasks[name] = get_tasks
        except Exception as e:
            logger.error(f"Error registering tasks {name}: {str(e)}")
            raise

    def get_user_constructor(self, name: str) -> Type[BaseUser]:
        if name not in self._users:
            raise KeyError(f"User {name} not found in registry")
        return self._users[name]

    def get_agent_constructor(self, name: str) -> Type[BaseAgent]:
        if name not in self._agents:
            raise KeyError(f"Agent {name} not found in registry. Available: {list(self._agents.keys())}")
        return self._agents[name]

    def get_env_constructor(self, name: str) -> Callable[[], Environment]:
        if name not in self._domains:
            raise KeyError(f"Domain {name} not found in registry")
        return self._domains[name]

    def get_tasks_loader(self, name: str) -> Callable[[], list[Task]]:
        if name not in self._tasks:
            raise KeyError(f"Task Set {name} not found in registry")
        return self._tasks[name]

    def get_users(self) -> list[str]:
        return list(self._users.keys())

    def get_agents(self) -> list[str]:
        return list(self._agents.keys())

    def get_domains(self) -> list[str]:
        return list(self._domains.keys())

    def get_task_sets(self) -> list[str]:
        return list(self._tasks.keys())

    def get_info(self) -> RegistryInfo:
        try:
            info = RegistryInfo(
                users=self.get_users(),
                agents=self.get_agents(),
                domains=self.get_domains(),
                task_sets=self.get_task_sets(),
            )
            return info
        except Exception as e:
            logger.error(f"Error getting registry info: {str(e)}")
            raise


from bench.agent.react_agent import ReActAgent
from bench.agent.function_calling_agent import FunctionCallingAgent
from bench.agent.plan_execute_agent import PlanExecuteAgent
from bench.domains.hr.environment import get_environment as hr_domain_get_environment
from bench.domains.hr.environment import get_tasks as hr_domain_get_tasks

try:
    registry = Registry()
    registry.register_user(DummyUser, "dummy_user")
    registry.register_agent(ReActAgent, "react_agent")
    registry.register_agent(FunctionCallingAgent, "fc_agent")
    registry.register_agent(PlanExecuteAgent, "plan_execute_agent")
    registry.register_domain(hr_domain_get_environment, "hr")
    registry.register_tasks(hr_domain_get_tasks, "hr")
except Exception as e:
    logger.error(f"Error initializing registry: {str(e)}")
