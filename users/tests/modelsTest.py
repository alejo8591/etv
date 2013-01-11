# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from users.models import CreateCodes, UserProfile

class UserProfileTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='80912071', email='alejo8591@gmail.com', password='123456789')

        self.userProfile = UserProfile.objects.create(identification=self.user)
        
    def testSaveUser(self):
        count_user = User.objects.count()
        users = User.objects.all()
        first_user = users[0]
        self.assertEqual(count_user,1)
        self.assertEqual(self.user.username, first_user.username)
        
    def testSaveUserProfile(self):
        count_userProfile = UserProfile.objects.count()
        usersProfile = UserProfile.objects.all()
        first_userProfile = usersProfile[0]
        self.assertEqual(count_userProfile,1)
        self.assertEqual(self.userProfile.identification, first_userProfile.identification)