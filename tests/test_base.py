"""
For Viable Industries, L.L.C. copyright information please see the LICENSE document
(the "License") included with this software package. This file may not
be used in any manner except in compliance with the License

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import rith
import unittest


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = rith.create_application(environment="testing")
        self.client = self.app.test_client()

    def test_api_client(self):
        self.assertIsNotNone(self.client)

    """Default Viable Data Tests."""
    def test_api_index(self):
        _response = self.client.get("/v1")
        self.assertEqual(_response.status_code, 200)

    def test_schema_user(self):
        model = app.schema.user.User(email="test.user@viable.io")
        self.assertIsNotNone(model)

    def test_schema_role(self):
        model = app.schema.role.Role
        self.assertIsNotNone(model)

    def test_schema_oauth_client(self):
        model_client = app.schema.client.Client()
        self.assertIsNotNone(model_client)

        model_grant = app.schema.grant.Grant()
        self.assertIsNotNone(model_grant)

        model_token = app.schema.token.Token()
        self.assertIsNotNone(model_token)

    def test_schema_create_role(self):
        role_ = app.schema.role.Role
        new_role_ = role_(name="test_role")
        self.assertIsNotNone(new_role_)

    def test_api_role_get_many(self):
        _response = self.client.get("/v1/data/role")
        self.assertEqual(_response.status_code, 403)

    def test_schema_create_user(self):
        user_ = app.schema.user.User
        new_user_ = user_(email="test.user@viable.io")
        self.assertIsNotNone(new_user_)

    def test_api_user_get_many(self):
        _response = self.client.get("/v1/data/user")
        self.assertEqual(_response.status_code, 403)

    def test_api_user_get_single(self):
        _response = self.client.get("/v1/data/user/1")
        self.assertEqual(_response.status_code, 403)


    """System-specific unit tests."""
    def test_schema_file(self):
        model = app.schema.file.File()
        self.assertIsNotNone(model)

    def test_schema_image(self):
        model = app.schema.image.Image()
        self.assertIsNotNone(model)
