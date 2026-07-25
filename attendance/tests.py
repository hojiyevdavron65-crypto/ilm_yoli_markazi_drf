from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Course, Group
from attendance.models import Attendance
import datetime

User = get_user_model()


class AttendanceAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", email="a@a.com", password="123", role=User.Role.ADMIN)
        self.teacher = User.objects.create_user(username="teacher", email="t@a.com", password="123", role=User.Role.TEACHER)
        self.student1 = User.objects.create_user(username="student1", email="s1@a.com", password="123", role=User.Role.STUDENT)
        self.student2 = User.objects.create_user(username="student2", email="s2@a.com", password="123", role=User.Role.STUDENT)

        self.course = Course.objects.create(name="Matematika")
        self.group = Group.objects.create(name="M-1", course=self.course, teacher=self.teacher)

        # Davomat ma'lumotlari
        self.attendance1 = Attendance.objects.create(
            group=self.group, student=self.student1, date=datetime.date.today(), is_present=True
        )
        self.attendance2 = Attendance.objects.create(
            group=self.group, student=self.student2, date=datetime.date.today(), is_present=False, reason="O'g'ri bo'lgan"
        )

        self.list_url = reverse("attendance-list")

    def test_student_sees_only_own_attendance(self):
        """O'quvchi faqat va faqat o'z davomatini ko'rishini tekshirish"""
        self.client.force_authenticate(user=self.student1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Jami 2 ta davomat yozuvi bor, lekin student1 faqat 1 tasini ko'rishi kerak
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["student"], self.student1.id)

    def test_student_cannot_create_attendance(self):
        """O'quvchi davomat belgiley olmasligini (403 Forbidden) tekshirish"""
        self.client.force_authenticate(user=self.student1)
        data = {
            "group": self.group.id,
            "student": self.student2.id,
            "date": str(datetime.date.today()),
            "is_present": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_attendance(self):
        """Ustoz davomat qila olishini tekshirish"""
        self.client.force_authenticate(user=self.teacher)
        data = {
            "group": self.group.id,
            "student": self.student1.id,
            "date": "2026-08-01",
            "is_present": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)