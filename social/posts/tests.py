from django.test import TestCase
from django.urls import reverse

from .models import Post, User, Group


class PostsTest(TestCase):
    def get_urls(self, post):
        urls = [
            reverse('index'),
            reverse('profile', kwargs={'username': post.author.username}),
            reverse('post', kwargs={'username': post.author.username,
                                    'post_id': post.id}),
        ]

        return urls

    def check_post_on_page(self, url, post):
        response = self.client.get(url)
        if 'paginator' in response.context:
            posts_list = response.context['paginator'].object_list
            self.assertEqual(len(posts_list), 1)
            self.assertEqual(posts_list[0], post)
        else:
            self.assertEqual(response.context['post'], post)

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')

    def test_profile_page_created(self):
        login = self.client.force_login(self.user)
        resp = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(resp.status_code, 200)

    def test_authenticated_user_can_post(self):
        login = self.client.force_login(self.user)
        resp = self.client.post(reverse('new_post'), {'text': 'hello'})
        self.assertEqual(resp.status_code, 302)

    def test_unauthenticated_user_cant_post(self):
        resp = self.client.get(reverse('new_post'))
        self.assertRedirects(resp, '/auth/login/?next=/new/')

    def test_new_post_appears_on_pages(self):
        login = self.client.force_login(self.user)
        # resp = self.client.post(reverse('new_post'), data={'text': 'hello'})
        post = Post.objects.create(text='hello', author=self.user)
        urls = self.get_urls(post=post)
        for url in urls:
            self.check_post_on_page(url=url, post=post)

    def test_authenticated_user_can_edit_post(self):
        login = self.client.force_login(self.user)
        group = Group.objects.create(title='edit_group', slug='edit-group')
        post = Post.objects.create(text='hello', group=group, author=self.user)
        resp = self.client.post(reverse('post_edit', kwargs={
            'username': post.author.username,
            'post_id': post.id
        }), data={'text': 'edited text'}, follow=True)
        post = Post.objects.get(id=post.id)
        urls = self.get_urls(post=post)
        for url in urls:
            self.check_post_on_page(url, post)
        resp = self.client.get(reverse('group', kwargs={'slug': group.slug}))
        self.assertNotIn(post, resp.context['paginator'].object_list)