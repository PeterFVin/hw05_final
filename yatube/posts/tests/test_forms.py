import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker

from core.test_utils import PostsTest
from posts.models import Comment, Group, Post


class FormTest(PostsTest):
    def test_post_create_form(self):
        """При отправке формы при создании поста создается запись в БД."""
        fake_data = Faker()
        test_image = fake_data.image()
        uploaded_image = SimpleUploadedFile(
            name='testimage.jpg',
            content=test_image,
            content_type='image/jpg',
        )
        data = {
            'group': self.group.id,
            'text': fake_data.text(),
            'image': uploaded_image,
        }

        self.author_client.post(
            reverse(self.ROUTES[5]['reverse']),
            data=data,
            follow=True,
        )
        edited_post = Post.objects.all().first()

        self.assertEqual(data['group'], edited_post.group.id)
        self.assertEqual(data['text'], edited_post.text)
        self.assertEqual(
            f'posts/{os.path.basename(edited_post.image.path)}',
            edited_post.image.name,
        )

    def test_post_create_form_guest(self):
        """При отправке формы без логина не создается запись в БД."""
        fake_data = Faker()
        data = {
            'group': self.group.id,
            'text': fake_data.text(),
        }

        self.client.post(
            reverse(self.ROUTES[5]['reverse']),
            data=data,
            follow=True,
        )
        counter = Post.objects.count()

        self.assertEqual(counter, 1)

    def test_post_edit_form(self):
        """Отправка формы при редактировании поста создается запись в БД."""
        fake_data = Faker()
        test_image = fake_data.image()
        uploaded_image = SimpleUploadedFile(
            name='testimage.jpg',
            content=test_image,
            content_type='image/jpg',
        )
        post = Post.objects.create(
            author=self.user,
            group=self.group,
            text=fake_data.text(),
        )
        edited_group = Group.objects.create(
            title=fake_data.first_name(),
            slug=fake_data.slug(),
            description=fake_data.text(),
        )

        data = {
            'group': edited_group.id,
            'text': fake_data.text(),
            'image': uploaded_image,
        }

        self.author_client.post(
            reverse(
                self.ROUTES[4]['reverse'],
                kwargs={'pk': f'{post.id}'},
            ),
            data=data,
            follow=True,
        )
        edited_post = Post.objects.get(id=post.id)

        self.assertEqual(post.author, edited_post.author)
        self.assertEqual(data['group'], edited_post.group.id)
        self.assertEqual(data['text'], edited_post.text)
        self.assertEqual(
            f'posts/{os.path.basename(edited_post.image.path)}',
            edited_post.image.name,
        )

    def test_post_edit_form_guest(self):
        """При отправке формы без логина не меняется запись в БД."""
        fake_data = Faker()
        post = Post.objects.create(
            author=self.user,
            group=self.group,
            text='текст не изменился',
        )
        edited_group = Group.objects.create(
            title=fake_data.first_name(),
            slug=fake_data.slug(),
            description=fake_data.text(),
        )

        data = {
            'group': edited_group.id,
            'text': fake_data.text(),
        }

        self.client.post(
            reverse(
                self.ROUTES[4]['reverse'],
                kwargs={'pk': f'{post.id}'},
            ),
            data=data,
            follow=True,
        )
        not_edited_post = Post.objects.get(id=post.id)

        self.assertEqual(not_edited_post.group.id, self.group.id)
        self.assertEqual(not_edited_post.text, 'текст не изменился')

    def test_post_edit_form_not_author(self):
        """При отправке формы не автором поста не меняется запись в БД."""
        fake_data = Faker()
        post = Post.objects.create(
            author=self.user,
            group=self.group,
            text='текст не изменился',
        )
        edited_group = Group.objects.create(
            title=fake_data.first_name(),
            slug=fake_data.slug(),
            description=fake_data.text(),
        )

        data = {
            'group': edited_group.id,
            'text': fake_data.text(),
        }

        self.authorized_client.post(
            reverse(
                self.ROUTES[4]['reverse'],
                kwargs={'pk': f'{post.id}'},
            ),
            data=data,
            follow=True,
        )
        not_edited_post = Post.objects.get(id=post.id)

        self.assertEqual(not_edited_post.group.id, self.group.id)
        self.assertEqual(not_edited_post.text, 'текст не изменился')

    def test_comment_form_authorized(self):
        """При отправке комментария под логином добавляется запись в БД."""
        fake_data = Faker()
        data = {
            'post': self.post,
            'group': self.group.id,
            'text': fake_data.text(),
            'author': self.user,
        }

        self.authorized_client.post(
            reverse('posts:add_comment', args=(self.post.id,)),
            data=data,
            follow=True,
        )
        counter = Comment.objects.count()
        self.assertEqual(counter, 1)

    def test_comment_form_guest(self):
        """При отправке комментария без логина не добавляется запись в БД."""
        fake_data = Faker()
        data = {
            'post': self.post,
            'group': self.group.id,
            'text': fake_data.text(),
            'author': self.user,
        }

        self.client.post(
            reverse('posts:add_comment', args=(self.post.id,)),
            data=data,
            follow=True,
        )
        counter = Comment.objects.count()
        self.assertEqual(counter, 0)
