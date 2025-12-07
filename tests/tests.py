from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

#Import relatif : rapport au fichier courant.
#   . : "le dossier courant"
#   .. : "le dossier parent"
from tasks.models import Task


class TaskModelTest(TestCase):
    def test_str_returns_title(self):
        task = Task(title="My task")

        self.assertEqual(str(task), "My task")


class TaskViewsTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Demo task")

    def test_homepage_renders(self):
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, 200)

    def test_create_task_via_post(self):
        response = self.client.post(reverse("list"), {"title": "New task"})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New task").exists())

    def test_update_page_renders(self):
        response = self.client.get(reverse("update_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_task_via_post(self):
        response = self.client.post(
            reverse("update_task", args=[self.task.id]),
            {"title": "Updated title"},
        )

        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    def test_delete_page_renders(self):
        response = self.client.get(reverse("delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_via_post(self):
        response = self.client.post(reverse("delete", args=[self.task.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

class TestDatasetLoading(TestCase):
    def test_load_initial_data(self):
        call_command('loaddata', 'dataset.json')

        self.assertEqual(Task.objects.count(), 3)
        titles = set(Task.objects.values_list("title", flat=True))
        self.assertSetEqual(
            titles,
            {"Configurer Ruff", "Ecrire des tests", "Preparer la release"},
        )