from typing import List
import logging
from .contracts import Task, TaskSource, check_task_source


logger = logging.getLogger(__name__)


class TaskProcessor:
    def __init__(self):
        self.sources = []
        logger.info('создан TaskProcessor')

    def add_source(self, source: TaskSource) -> bool:
        if check_task_source(source):
            self.sources.append(source)
            logger.info(f'Источник {source} добавлен')
            return True
        else:
            logger.error(f'Источник {source} не соответствует контракту')
            return False

    def process_all(self) -> List[Task]:
        all_tasks = []


        for i, source in enumerate(self.sources, 1):
            logger.info(f'Обработка источника {i}/{len(self.sources)}: {source}')

            try:
                tasks = source.get_tasks()
                logger.info(f'Получено {len(tasks)} задача из источника {source}')
                for task in tasks:
                    logger.debug(f'Задача: {task}')
                all_tasks.extend(tasks)
            except Exception as e:
                logger.error(f'Ошибка при получении задач: {e}')
                continue

        logger.info(f'Всего получено задач: {len(all_tasks)}')
        return all_tasks

    def get_sorce_count(self) -> int:
        return len(self.sources)