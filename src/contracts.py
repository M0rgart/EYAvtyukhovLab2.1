import logging
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


logger = logging.getLogger(__name__)


@dataclass
class Task:
    id: int
    payload: any

    def __repr__(self):
        return f"Task(id={self.id}, payload={self.payload})"


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> list[Task]:
        pass

    def __repr__(self) -> str:
        pass


def check_task_source(task: any) -> bool:
    if isinstance(task, TaskSource):
        logger.info(f"Объект {task} является TaskSource")
    else:
        logger.warning(f"Объект {task} не является TaskSource")

    if hasattr(task, "get_tasks"):
        logger.info(f"Объект {task} имеет атрибут get_tasks")
    else:
        logger.warning(f"Объект {task} не имеет атрибута get_tasks")

    return isinstance(task, TaskSource)