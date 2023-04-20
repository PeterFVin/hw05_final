from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from faker import Faker

from posts.models import Group, Post, User


class PostsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fake_data = Faker()
        test_image = fake_data.image()
        cls.uploaded_image = SimpleUploadedFile(
            name='testimage.jpg',
            content=test_image,
            content_type='image/jpg',
        )
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
            image=cls.uploaded_image,
        )
        cls.ROUTES = (
            {
                'post on page': True,
                'reverse': 'posts:index',
                'template': 'posts/index.html',
                'url': '/',
            },
            {
                'post on page': True,
                'pars': [cls.group.slug],
                'reverse': 'posts:group_list',
                'template': 'posts/group_list.html',
                'url': f'/group/{cls.group.slug}/',
            },
            {
                'post on page': True,
                'pars': [cls.user],
                'reverse': 'posts:profile',
                'template': 'posts/profile.html',
                'url': f'/profile/{cls.user}/',
            },
            {
                'pars': [cls.post.id],
                'reverse': 'posts:post_detail',
                'template': 'posts/post_detail.html',
                'url': f'/posts/{cls.post.id}/',
            },
            {
                'authorised_user': True,
                'reverse': 'posts:post_create',
                'template': 'posts/create_post.html',
                'url': '/create/',
            },
        )

    def setUp(self):
        self.authorized_user = User.objects.create(username='authorized_user')

        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)

        self.author_client = Client()
        self.author_client.force_login(self.user)

    def get_client(self, route):
        if route.get('author'):
            return self.author_client
        elif route.get('authorised_user'):
            return self.authorized_client
        return self.client
