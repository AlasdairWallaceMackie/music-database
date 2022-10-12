from platform import release
from django.test import TestCase, Client

from datetime import date

from ..login_and_reg_app.models import *
from .models import *

class BaseTestCase(TestCase):
    def setUp(self):
        self.test_users = []
        self.test_bands = []

        usernames = ["test_user1", "test_user2", "test_user3"]

        for user in usernames:
            new_user = User.objects.create(
                username = user,
                email = f"{user}@test.org",
                password = "password",
            )
            self.test_users.append(new_user)

        for i in range(1,4):
            new_band = Band.objects.create(
                name = f"test_band{i}",
                genre = "Test Genre",
                founded = "2013",
                country = "US",
                status = 2,
                added_by = self.test_users[0],
                last_edited_by = self.test_users[0],
            )
            self.test_bands.append(new_band)

        self.test_album = Album.objects.create(
            title = "test_album",
            band = self.test_bands[0],
            release_date = date.today(),
            added_by = self.test_users[0],
            last_edited_by = self.test_users[0]
        )

        self.c = Client()

        # user = self.test_users[0]

        # print("User info:")
        # print(f"Total contributions: {user.total_contributions()}")
        # print(f"Bands added: {user.number_of_bands_added()}")
        # print(f"Albums added: {user.number_of_albums_added()}")

    def test_setUp(self):
        self.assertEqual(self.test_users[2].email, "test_user3@test.org")
        self.assertEqual(self.test_bands[2].name, "test_band3")

    def test_base_user_functions_empty(self):
        user = self.test_users[1]
        
        self.assertEqual(user.added_bands.count(), 0)
        self.assertEqual(user.added_albums.count(), 0)

        # self.assertEqual(int(user.total_contributions()), 0)
        self.assertEqual(user.number_of_bands_added(), 0)
        self.assertEqual(user.number_of_albums_added(), 0)

    def test_create_band(self):
        data = {
            'name': "test_create_band",
            'genre': "Test Create Band Genre",
            'founded': 2013,
            'country': "US",
            'status': 0,
            'added_by': self.test_users[0],
            'last_edited_by': self.test_users[0],
        }
        self.c.post("bands/create/", data)
        new_band = Band.objects.latest('created_at')

        self.assertEqual(new_band.name, data['name'])
    
    def test_create_album(self):
        data = {
            'title': "test_create_album",
            'band': self.test_bands[0],
            'release_date': date.today(),
            'added_by': self.test_users[0],
            'last_edited_by': self.test_users[0],
        }
        self.c.post("bands/create/", data)
        new_album = Band.objects.latest('created_at')

        self.assertEqual(new_album.title, data['title'])

    def test_rate_album(self):
        id = 1

        data = {
            'value': 5,
            'album': Album.objects.get(id=id),
            'user': self.test_users[0],

        }
        self.c.post(f"albums/{id}/rate", data)
        new_rating = Rating.objects.latest('created_at')

        self.assertEqual(new_rating.value, 5)

    def test_login(self):
        response = self.c.post("login/", {'username': self.test_users[0].username, 'password': "password"})
        
        self.assertIsNotNone(response)
