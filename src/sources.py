import logging
import json, random, string
from .contracts import Task, TaskSource
from typing import List, Generator


logger = logging.getLogger(__name__)


class FileTaskSource:
    def __init__(self, path: str):
        self.path = path
        logger.info(f"Создан FileTaskSource с фалом {path}")

    def _generate_id(self) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    def get_tasks(self) -> List[Task]:
        try:
            with open(self.path, 'r', encoding="utf-8") as f:
                data = json.load(f)

            tasks = []
            for item in data:
                task = Task(id=item.get('id', self._generate_id()),
                            payload=item.get('payload', {}))
                tasks.append(task)

            logger.info(f"Загружено {len(tasks)} задач из файла {self.path}")
            return tasks

        except FileNotFoundError:
            logger.error(f"Файл {self.path} не найден")
            raise FileNotFoundError(f"Файл {self.path} не найден")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON в файле {self.path}: {e}")
            raise json.JSONDecodeError(f"Ошибка парсинга JSON в файле {self.path}: {e}")
        except Exception as e:
            logger.error(f"Не предвиденная ошибка: {e}")
            raise

    def __repr__(self):
        return f"FileTaskSource(path={self.path})"


class GeneratorTaskSource:
    def __init__(self, count: int=10, pref: str='gen'):
        self.count = count
        self.pref = pref
        logger.info(f"Создан GeneratorTaskSource (count={self.count}, pref={self.pref})")

    def get_tasks(self) -> List[Task]:
        tasks = []
        for i in range(self.count):
            task = Task(
                id=f'{self.pref}_{i+1}',
                payload={
                    'number': i+1,
                    'data': random.randint(1, 100000),
                    'timestamp': f"2026-02{i+1:02d}"
                }
            )
            tasks.append(task)

        logger.info(f"Сгенерированно {len(tasks)} задач")
        return tasks

    def __repr__(self):
        return f"GeneratorTaskSource(count={self.count}, pref={self.pref})"


class APITaskSource:
    def __init__(self, end: str='https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
        self.end = end
        self._tasks = self._generate_mock_tasks()
        logger.info(f"Создан APITaskSource с эндпоинтом {self.end}")

    def get_tasks(self) -> List[Task]:
        logger.debug(f'Выполняется запрос к {self.end}')
        logger.info(f'Получено {len(self._tasks)} задач из API')
        return self._tasks.copy()

    def _generate_mock_tasks(self) -> List[Task]:
        tasks = []
        for i in range(5):
            task = Task(
                id=f"api_{i+1}",
                payload={
                    'topic': random.choice(["1", "2", "3", "4", "5"]),
                    'dif': random.choice(['low', 'medium', 'high']),
                    'points': random.randint(10, 100)
                }
            )
            tasks.append(task)
        return tasks

    def __repr__(self):
        return f"APITaskSource(endpoint={self.end})"
