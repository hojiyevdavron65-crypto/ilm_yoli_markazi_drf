from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Course, Group
from grading.models import Grade

User = get_user_model()


class GradingAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", email="a@a.com", password="123", role=User.Role.ADMIN)
        self.teacher = User.objects.create_user(username="teacher", email="t@a.com", password="123",
                                                role=User.Role.TEACHER)

        self.student1 = User.objects.create_user(username="student1", email="s1@a.com", password="123",
                                                 role=User.Role.STUDENT)
        self.student2 = User.objects.create_user(username="student2", email="s2@a.com", password="123",
                                                 role=User.Role.STUDENT)

        self.course = Course.objects.create(name="Python Backend")
        self.group = Group.objects.create(name="PY-01", course=self.course, teacher=self.teacher)

        # Baholar yaratamiz
        self.grade1 = Grade.objects.create(group=self.group, student=self.student1, grade=95, comment="A'lo")
        self.grade2 = Grade.objects.create(group=self.group, student=self.student2, grade=70, comment="Yaxshi")

        self.list_url = reverse("grade-list")

    def test_student_sees_only_own_grades(self):
        """O'quvchi faqat va faqat o'zining bahosini ko'rishini tekshirish"""
        self.client.force_authenticate(user=self.student1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Baza 2 ta baho bor, lekin student1 faqat 1 tasini ko'rishi shart!
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["grade"], 95)
        self.assertEqual(response.data[0]["student"], self.student1.id)

    def test_student_cannot_add_grade(self):
        """O'quvchi o'ziga yoki boshqalarga baho qo'yo olmasligini (403 Forbidden) tekshirish"""
        self.client.force_authenticate(user=self.student1)
        data = {
            "group": self.group.id,
            "student": self.student1.id,
            "grade": 100,
            "comment": "O'zimga o'zim 100 qo'ydim"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_add_grade(self):
        """Ustoz o'quvchiga baho qo'ya olishini tekshirish"""
        self.client.force_authenticate(user=self.teacher)
        data = {
            "group": self.group.id,
            "student": self.student2.id,
            "grade": 85,
            "comment": "Uy vazifasi uchun"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 3)