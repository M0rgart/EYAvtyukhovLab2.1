import unittest, json, os
import tempfile, logging
from src.sources import FileTaskSource, GeneratorTaskSource, APITaskSource


logging.disable(logging.CRITICAL)


class TestSources(unittest.TestCase):

    def setUp(self):
        """Подготовка к тестам"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()

    def tearDown(self):
        """Очистка после тестов"""
        os.unlink(self.temp_file.name)

    def test_file_source_valid(self):
        """Тест FileTaskSource с корректным файлом"""
        test_data = [
            {"id": "task1", "payload": {"value": 100}},
            {"id": "task2", "payload": {"value": 200}}
        ]

        with open(self.temp_file.name, 'w') as f:
            json.dump(test_data, f)

        source = FileTaskSource(self.temp_file.name)
        tasks = source.get_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, "task1")
        self.assertEqual(tasks[0].payload, {"value": 100})

    def test_file_source_missing_id(self):
        """Тест FileTaskSource с отсутствующими ID"""
        test_data = [
            {"payload": {"value": 100}},
            {"payload": {"value": 200}}
        ]

        with open(self.temp_file.name, 'w') as f:
            json.dump(test_data, f)

        source = FileTaskSource(self.temp_file.name)
        tasks = source.get_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertIsNotNone(tasks[0].id)
        self.assertIsNotNone(tasks[1].id)

    def test_file_source_not_found(self):
        """Тест FileTaskSource с несуществующим файлом"""
        source = FileTaskSource("nonexistent.json")

        with self.assertRaises(FileNotFoundError):
            source.get_tasks()

    def test_generator_source(self):
        """Тест GeneratorTaskSource"""
        source = GeneratorTaskSource(count=5, pref="test")
        tasks = source.get_tasks()

        self.assertEqual(len(tasks), 5)
        for i, task in enumerate(tasks, 1):
            self.assertEqual(task.id, f"test_{i}")
            self.assertIn('number', task.payload)
            self.assertIn('data', task.payload)
            self.assertIn('timestamp', task.payload)

    def test_api_source(self):
        """Тест APITaskSource"""
        source = APITaskSource()
        tasks = source.get_tasks()

        self.assertEqual(len(tasks), 5)
        for task in tasks:
            self.assertTrue(task.id.startswith("api_"))
            self.assertIn('topic', task.payload)
            self.assertIn('dif', task.payload)
            self.assertIn('points', task.payload)

    def test_source_repr(self):
        """Тест строкового представления источников"""
        file_source = FileTaskSource("test.json")
        gen_source = GeneratorTaskSource(count=3)
        api_source = APITaskSource()

        self.assertIn("FileTaskSource", repr(file_source))
        self.assertIn("GeneratorTaskSource", repr(gen_source))
        self.assertIn("APITaskSource", repr(api_source))


if __name__ == '__main__':
    unittest.main()