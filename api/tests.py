# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
#
# from .models import Instance
# from .models import CrawlSystem
# from django.contrib.auth.models import User
#
# from .serializers import InstanceSerializer
# from .serializers import CrawlInstanceSerializer
# import json
#
#
# # tests for views
#
#
# class BaseViewTest(APITestCase):
#     client = APIClient()
#
#     def login_client(self, username="", password=""):
#         # get a token from DRF
#         response = self.client.post(
#             reverse('create-token'),
#             data=json.dumps(
#                 {
#                     'username': username,
#                     'password': password
#                 }
#             ),
#             content_type='application/json'
#         )
#         self.token = response.data['token']
#         # set the token in the header
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer ' + self.token
#         )
#         self.client.login(username=username, password=password)
#         return self.token
#
#     @staticmethod
#     def create_instance(instance_id="", region="", pem_file="", _type=''):
#         if instance_id != "" and region != "" and pem_file != "" and _type != '':
#             Instance.objects.create(aws_instance_id=instance_id, aws_region_name=region, pem_file=pem_file,
#                                     system_type=_type)
#
#     @staticmethod
#     def create_crawl_system(state="", id=None, ip=""):
#         if state != "" and id != "" and ip != "":
#             CrawlSystem.objects.create(instance_state=state, instance_id=id, instance_ip=ip)
#
#     def login_a_user(self, username="", password=""):
#         url = reverse(
#             "auth-login",
#             kwargs={
#                 "version": "v1"
#             }
#         )
#         return self.client.post(
#             url,
#             data=json.dumps({
#                 "username": username,
#                 "password": password
#             }),
#             content_type="application/json"
#         )
#
#     def setUp(self):
#         # add test data
#         self.user = User.objects.create_superuser(
#             username="test_user",
#             email="test@mail.com",
#             password="testing",
#             first_name="test",
#             last_name="user",
#         )
#
#         self.create_instance("i-1234", "region-1", "pem_file.pem", 'type1')
#         self.create_instance("1-2345", "region-2", "pem_file.pem", 'type1')
#         self.create_instance("1-3456", "region-2", "pem_file1.pem", 'type2')
#         ins_obj = Instance.objects.first()
#         ins_obja = Instance.objects.all()
#
#         self.create_crawl_system('running', ins_obj, '1.2.3.4')
#         self.create_crawl_system('stopped', ins_obja[2], '1.2.6.4')
#         self.create_crawl_system('running', ins_obj, '1.2.7.4')
#
#
# class AllTestCases(BaseViewTest):
#
#     def test_get_all_instance(self):
#         """
#         This test ensures that all songs added in the setUp method
#         exist when we make a GET request to the songs/ endpoint
#         """
#         # hit the API endpoint
#         self.login_client('test_user', 'testing')
#         api_endpoint = "instance-all"
#         response = self.client.get(
#             reverse(api_endpoint)
#         )
#         # fetch the data from db
#         expected = Instance.objects.all()
#         print(expected)
#         serialized = InstanceSerializer(expected, many=True)
#         self.assertEqual(response.data, serialized.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print("Test Case for API endpoint {} Done".format(api_endpoint))
#
#         api_endpoint = "crawl_system-all"
#         response = self.client.get(
#             reverse(api_endpoint)
#         )
#         ins_obj = Instance.objects.first()
#         # fetch the data from db
#         expected = CrawlSystem.objects.all()
#         print(expected)
#         serialized = CrawlInstanceSerializer(expected, many=True)
#         self.assertEqual(response.data, serialized.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print("Test Case for API endpoint {} Done".format(api_endpoint))
#
#         """
#         This test ensures that all songs added in the setUp method
#         exist when we make a GET request to the songs/ endpoint
#         """
#         # hit the API endpoint
#
#     class AuthLoginUserTest(BaseViewTest):
#         """
#         Tests for the auth/login/ endpoint
#         """
#
#         def test_login_user_with_valid_credentials(self):
#             # test login with valid credentials
#             response = self.login_a_user("test_user", "testing")
#             # assert token key exists
#             self.assertIn("token", response.data)
#             # assert status code is 200 OK
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             # test login with invalid credentials
#             response = self.login_a_user("anonymous", "pass")
#             # assert status code is 401 UNAUTHORIZED
#             self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
