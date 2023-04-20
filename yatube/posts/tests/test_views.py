from http import HTTPStatus
from math import ceil

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.test import Client
from django.urls import reverse

from core.tests.test_utils import PostsTest
from posts.models import Follow, Post, User

PAGINATOR_NUM_POSTS = settings.NUM_OBJ_ON_PAGE + 2


class ViewTest(PostsTest):
    def test_reverses(self):
        """URL-адреса используют соответствующие шаблоны."""
        cache.clear()
        for route in self.ROUTES:
            with self.subTest(
                reverse=route['reverse'],
                template=route['template'],
            ):
                current_client = self.get_client(route)
            response = current_client.get(
                reverse(route['reverse'], args=route.get('pars')),
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertTemplateUsed(response, route['template'])

    def test_created_post_in_pages(self):
        """Пост отображается на страницах index, group_list, profile."""
        cache.clear()
        for page in self.ROUTES:
            if 'post on page' in page:
                url = page['url']
                with self.subTest(url=url):
                    response = self.client.get(url)
                    posts = response.context['page_obj']
                    self.assertIn(self.post, posts)
                    self.assertEqual(len(posts), 1)

    def test_post_in_right_group(self):
        """Созданный пост с указанной группой принадлежит этой группе."""
        response = self.post.group.id
        self.assertEqual(response, self.group.id)

    def test_index_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(
            reverse(self.ROUTES[0]['reverse']),
        )
        self.assertEqual(response.context['post'].author, self.user)
        self.assertEqual(response.context['post'].text, 'Тестовый пост')
        self.assertEqual(response.context['post'].group, self.group)
        self.assertEqual(response.context['post'].image, self.post.image.name)

    def test_group_list_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                self.ROUTES[1]['reverse'],
                kwargs={'slug': f'{self.group.slug}'},
            ),
        )
        self.assertEqual(response.context['post'].author, self.user)
        self.assertEqual(response.context['post'].text, 'Тестовый пост')
        self.assertEqual(response.context['post'].group, self.group)
        self.assertEqual(response.context['post'].image, self.post.image.name)

    def test_profile_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                self.ROUTES[2]['reverse'],
                kwargs={'username': f'{self.user}'},
            ),
        )
        self.assertEqual(response.context['post'].author, self.user)
        self.assertEqual(response.context['post'].text, 'Тестовый пост')
        self.assertEqual(response.context['post'].group, self.group)
        self.assertEqual(response.context['post'].image, self.post.image.name)

    def test_post_detail_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                self.ROUTES[3]['reverse'],
                kwargs={'pk': f'{self.post.id}'},
            ),
        )
        self.assertEqual(response.context['post'].author, self.user)
        self.assertEqual(response.context['post'].text, 'Тестовый пост')
        self.assertEqual(response.context['post'].group, self.group)
        self.assertEqual(response.context['post'].image, self.post.image.name)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.author_client.get(
            reverse(
                self.ROUTES[4]['reverse'],
                kwargs={'pk': f'{self.post.id}'},
            ),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(self.ROUTES[5]['reverse']),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response = self.authorized_client.get(reverse('posts:index'))
        posts = response.content
        Post.objects.create(
            text='test_new_post',
            author=self.user,
        )
        response_old = self.authorized_client.get(reverse('posts:index'))
        old_posts = response_old.content
        self.assertEqual(old_posts, posts)
        cache.clear()
        response_new = self.authorized_client.get(reverse('posts:index'))
        new_posts = response_new.content
        self.assertNotEqual(old_posts, new_posts)

    def test_authorized_user_following(self):
        """Авторизованный пользователь может подписываться и отписываться."""
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user.username},
            ),
        )
        counter = Follow.objects.filter(author=self.user).count()
        self.assertEqual(counter, 1)

        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user.username},
            ),
        )
        counter = Follow.objects.filter(author=self.user).count()
        self.assertEqual(counter, 0)

    def test_follower_feed_ok(self):
        """Новая запись автора появляется в ленте фолловера."""
        Follow.objects.create(user=self.user, author=self.user)
        follower = Client()
        follower.force_login(self.user)
        response_follower = follower.get(reverse('posts:follow_index'))
        context_follower = response_follower.context['page_obj'].object_list[0]
        self.assertEqual(context_follower, self.post)

    def test_not_followier_feed_not_ok(self):
        """Новая запись автора не появляется в ленте неподписавшегося."""
        unfollow_user = User.objects.create(username='unfollow_user')
        Follow.objects.create(user=self.user, author=self.user)
        unfollower = Client()
        unfollower.force_login(unfollow_user)
        response_unfollower = unfollower.get(reverse('posts:follow_index'))
        self.assertEqual(len(response_unfollower.context['page_obj']), 0)


class PaginatorTest(PostsTest):
    def test_paginator(self):
        """Проверка пагинатора на страницах index, group_list, profile."""

        pages_num = ceil(PAGINATOR_NUM_POSTS / settings.NUM_OBJ_ON_PAGE)

        num_posts_last_page = (
            PAGINATOR_NUM_POSTS - settings.NUM_OBJ_ON_PAGE * (pages_num - 1)
        )

        posts = [
            Post(
                author=self.user,
                group=self.group,
                text=f'Тестовый пост № {obj+2}',
            )
            for obj in range(PAGINATOR_NUM_POSTS - 1)
        ]
        Post.objects.bulk_create(posts)

        for page in self.ROUTES:
            # Проводим тест только для тех страниц, у которых есть паджинатор
            if 'post on page' in page:
                url = page['url']
                # Проводим тест для нескольких страниц каждого url
                for page_num in range(1, pages_num + 1):
                    response = self.client.get(f'{url}?page={page_num}')
                    # При запросе авторизации, на странице не будет контекста
                    if not response.context:
                        continue
                    page_obj = response.context.get('page_obj', False)
                    if not page_obj:
                        continue
                    if page_num == pages_num:
                        self.assertEqual(
                            len(page_obj.object_list),
                            num_posts_last_page,
                        )
                    else:
                        self.assertEqual(
                            len(page_obj.object_list),
                            settings.NUM_OBJ_ON_PAGE,
                        )
