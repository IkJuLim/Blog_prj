from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models imort Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 네비게이션 바가 있다.
        navbar = soup.nav
        # 1.5 Blog, About_Me 라는 문구가 네베게이션에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About_Me', navbar.text)

        # 2.1 포스트가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 main area에 '아직 게시물이 없습니다'라는 문구가 나타난다.
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3.1 포스트가 2개 있다면
        post_001 = Post.objects.creat(
            title = '첫 번째 포스트 입니다.',
            content = 'Hello World. We are the world.'
        )
        post_002 = Post.objects.creat(
            title = '두 번째 포스트 입니다.',
            content = '1등이 전부는 아니잖아.'
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트 목록 페이지를 새로고침 했늘때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 main area에 포스트2개의 제목이 존재한다.
        main_area = soup.find('div', id = 'main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 없습니다'라는 뭉구가 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)