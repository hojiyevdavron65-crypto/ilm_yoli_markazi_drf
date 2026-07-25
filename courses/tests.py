from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Group

User = get_user_model()


class CoursesAPITests(APITestCase):

    def setUp(self):
        # 1. Admin yaratamiz
        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="Password123!",
            role=User.Role.ADMIN
        )

        # 2. Ustozlarni yaratamiz
        self.teacher1 = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="Password123!",
            role=User.Role.TEACHER
        )
        self.teacher2 = User.objects.create_user(
            username="teacher2",
            email="teacher2@example.com",
            password="Password123!",
            role=User.Role.TEACHER
        )

        # 3. O'quvchi yaratamiz
        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Password123!",
            role=User.Role.STUDENT
        )

        # 4. Boshlang'ich Kurs va Guruhlar
        self.course = Course.objects.create(
            name="Python Django",
            description="Backend kursi"
        )
        self.group1 = Group.objects.create(
            name="FN-1",
            course=self.course,
            teacher=self.teacher1
        )
        self.group2 = Group.objects.create(
            name="FN-2",
            course=self.course,
            teacher=self.teacher2
        )

        # URL larni olish
        self.course_list_url = reverse("course-list")
        self.group_list_url = reverse("group-list")

    def test_admin_can_create_course(self):
        """Admin yangi kurs yarata olishini tekshirish"""
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "English IELTS", "description": "General English"}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_student_cannot_create_course(self):
        """O'quvchi kurs yarata olmasligini (403 Forbidden) tekshirish"""
        self.client.force_authenticate(user=self.student)
        data = {"name": "Matematika", "description": "Oliy matematika"}
        response = self.client.post(self.course_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_sees_only_own_groups(self):
        """Ustoz faqat o'zi dars beradigan guruhni ko'rishini tekshirish"""
        self.client.force_authenticate(user=self.teacher1)
        response = self.client.get(self.group_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.group1.id)

    def test_admin_and_student_can_see_all_groups(self):
        """Admin barcha guruhlarni ko'ra olishini tekshirish"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.group_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)