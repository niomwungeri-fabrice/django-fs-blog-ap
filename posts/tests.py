from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from faker import Faker
from django.urls import reverse
faker = Faker()
# Create your tests here.


class BlogTests(TestCase):
    body = faker.text()
    title = faker.sentence()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='password123',
            email=faker.email()
        )
        self.post = Post.objects.create(
            title=self.title,
            body=self.body,
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='title')
        self.assertEqual(str(post), post.title)

    def test_content(self):
        self.assertEqual(self.title, self.post.title)
        self.assertEqual(self.post.body, self.body)

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.body)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view_successfully(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.body)

    def test_post_detail_view(self):
        response = self.client.get(
            '/post/{}/'.format(faker.random_int(100, 10000)))
        self.assertEqual(response.status_code, 404)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_create_view(self):
        payload = {
            'title': self.title,
            'body': self.body,
            'author': self.user
        }
        response = self.client.post('/post/new/', payload)
        response_reverse = self.client.post(reverse('post_new'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_reverse.status_code, 200)

    def test_post_update_view(self):
        payload = {
            'title': faker.sentence(),
            'body': faker.text(),
        }
        response_reverse = self.client.post(
            reverse('post_edit', args=str(self.post.id)),
            payload)
        self.assertEqual(response_reverse.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(
            reverse('post_delete', args=str(self.post.id)))
        self.assertEqual(response.status_code, 200)
