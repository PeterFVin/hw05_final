from http import HTTPStatus

from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class UrlTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )
        cls.urls = {
            'comment': reverse('posts:add_comment', args=(cls.post.id,)),
            'follow': reverse('posts:follow_index'),
            'group': reverse('posts:group_list', args=(cls.group.slug,)),
            'index': reverse('posts:index'),
            'post_create': reverse('posts:post_create'),
            'post_edit': reverse('posts:post_edit', args=(cls.post.id,)),
            'post_detail': reverse('posts:post_detail', args=(cls.post.id,)),
            'profile': reverse('posts:profile', args=(cls.user,)),
            'profile_follow': reverse(
                'posts:profile_follow', args=(cls.user,),
            ),
            'profile_unfollow': reverse(
                'posts:profile_unfollow', args=(cls.user,),
            ),
            'missing': '/unexisting_page/',
        }

        cls.authorized_user = User.objects.create_user(
            username='authorized_user',
        )

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.authorized_user)

        cls.author_client = Client()
        cls.author_client.force_login(cls.user)

    def test_http_statuses(self) -> None:
        """Доступность URL-адресов."""
        httpstatuses = (
            (self.urls.get('comment'), HTTPStatus.FOUND, self.client),
            (self.urls.get('follow'), HTTPStatus.FOUND, self.client),
            (self.urls.get('group'), HTTPStatus.OK, self.client),
            (self.urls.get('index'), HTTPStatus.OK, self.client),
            (self.urls.get('post_create'), HTTPStatus.FOUND, self.client),
            (
                self.urls.get('post_create'),
                HTTPStatus.OK,
                self.authorized_client,
            ),
            (self.urls.get('post_edit'), HTTPStatus.FOUND, self.client),
            (
                self.urls.get('post_edit'),
                HTTPStatus.FOUND,
                self.authorized_client,
            ),
            (self.urls.get('post_edit'), HTTPStatus.FOUND, self.author_client),
            (self.urls.get('post_detail'), HTTPStatus.OK, self.client),
            (self.urls.get('profile'), HTTPStatus.OK, self.client),
            (self.urls.get('profile_follow'), HTTPStatus.FOUND, self.client),
            (self.urls.get('profile_unfollow'), HTTPStatus.FOUND, self.client),
            (self.urls.get('missing'), HTTPStatus.NOT_FOUND, self.client),
        )

        for url, status, client in httpstatuses:
            with self.subTest():
                self.assertEqual(client.get(url).status_code, status)

    def test_templates(self) -> None:
        cache.clear()
        templates = (
            (
                self.urls.get('follow'),
                'posts/follow.html',
                self.authorized_client,
            ),
            (self.urls.get('group'), 'posts/group_list.html', self.client),
            (self.urls.get('index'), 'posts/index.html', self.client),
            (
                self.urls.get('post_create'),
                'posts/create_post.html',
                self.authorized_client,
            ),
            (
                self.urls.get('post_detail'),
                'posts/post_detail.html',
                self.client,
            ),
            (self.urls.get('profile'), 'posts/profile.html', self.client),
            (self.urls.get('missing'), 'core/404.html', self.client),
        )

        for url, template, client in templates:
            with self.subTest():
                self.assertTemplateUsed(client.get(url), template)

    def test_redirects(self) -> None:
        redirects = (
            (
                self.urls.get('comment'),
                f'/posts/{self.post.id}/comment/',
                self.client,
            ),
            (self.urls.get('post_create'), '/create/', self.client),
            (
                self.urls.get('post_edit'),
                f'/posts/{self.post.id}/edit/',
                self.client,
            ),
            (
                self.urls.get('post_edit'),
                f'/posts/{self.post.id}/',
                self.authorized_client,
            ),
            (
                self.urls.get('profile_follow'),
                f'/profile/{self.user}/follow/',
                self.client,
            ),
            (
                self.urls.get('profile_unfollow'),
                f'/profile/{self.user}/unfollow/',
                self.client,
            ),
        )

        for url, redirect, client in redirects:
            with self.subTest():
                url = client.get(url)
                if client == self.client:
                    self.assertRedirects(url, redirect_to_login(redirect).url)
                else:
                    self.assertRedirects(url, redirect)
