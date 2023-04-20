from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

from posts.models import Group, Post

User = get_user_model()

fake = Faker()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title=fake.first_name(),
            slug=fake.slug(),
            description=fake.text(),
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=fake.text(),
        )

    def test_post_model_have_correct_object_names(self):
        """Проверяем, что у модели post корректно работает __str__."""
        self.assertEqual(
            str(self.post),
            self.post.text[
                :settings.MODEL_STR_REPRESENTATION_LIMIT
            ],  # fmt: skip
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'text': 'текст поста',
            'author': 'автор',
            'group': 'группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name,
                    expected_value,
                )

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'введите текст поста',
            'group': 'группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text,
                    expected_value,
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title=fake.first_name(),
            slug=fake.slug(),
            description=fake.text(),
        )

    def test_group_models_have_correct_object_names(self):
        """Проверяем, что у модели group корректно работает __str__."""
        self.assertEqual(str(self.group), self.group.title)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'description': 'описание',
            'slug': 'ссылка',
            'title': 'название',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Group._meta.get_field(field).verbose_name,
                    expected_value,
                )
