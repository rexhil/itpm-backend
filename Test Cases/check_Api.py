import requests
import unittest

base_url = 'http://127.0.0.1:8000'


def get_csrf(client):
    if 'csrftoken' in client.cookies:
        csrftoken = client.cookies['csrftoken']
    else:
        csrftoken = client.cookies['csrf']
    client.headers.update({'X-CSRFToken': csrftoken})
    return client, csrftoken


def python_request_login():
    client = requests.session()
    login_url = '{}/login/'.format(base_url)
    client.get(login_url)
    # Get CSRF Before Login
    client, csrftoken = get_csrf(client)

    login_data = dict(username='rexhil', password='97a177a5e1', csrfmiddlewaretoken=csrftoken)
    client.post(login_url, data=login_data, headers=dict(Referer=login_url), allow_redirects=False)
    # Get CSRF After Login
    client, csrftoken = get_csrf(client)

    return client, csrftoken

class LoginTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_Login(self):
        self.assertEqual(200, python_request_login(True))

    def test_not_login(self):
        self.assertNotEqual(200, python_request_login(False))


# class CrawlSystemTest(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_insert(self):
#         self.assertEqual(201, insert_crawl_system())
#
#     def test_update(self):
#         self.assertEqual(200, update_crawl_system())


# class InputTableTest(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_get_data(self):
#         self.assertEqual(200, get_input_data())


if __name__ == '__main__':
    unittest.main()
    # get_input_data()
