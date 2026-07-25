from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Course, Group
from enrollment.models import EnrollmentRequest, GroupStudent

User = get_user_model()


class EnrollmentViewDetailTests(APITestCase):

    def setUp(self):
        # Admin, Ustoz va Student yaratamiz
        self.admin = User.objects.create_user(username="admin", password="123", role=User.Role.ADMIN)
        self.student = User.objects.create_user(username="student", password="123", role=User.Role.STUDENT)
        self.other_student = User.objects.create_user(username="other_student", password="123", role=User.Role.STUDENT)

        self.course = Course.objects.create(name="Python")
        self.group = Group.objects.create(name="P-1", course=self.course)

        # Ariza yaratamiz
        self.enrollment = EnrollmentRequest.objects.create(student=self.student, group=self.group)

    def test_student_cannot_approve_enrollment_view(self):
        """View testi: Student arizani tasdiqlamoqchi bo'lsa 403 Forbidden berishi kerak"""
        self.client.force_authenticate(user=self.student)
        url = reverse("enrollment-approve", kwargs={"pk": self.enrollment.id})

        response = self.client.patch(url)

        # View status kodi 403 bo'lishini tekshiramiz
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_sees_only_own_enrollments_in_queryset(self):
        """View testi: get_queryset studentga faqat o'z arizalarini ko'rsatishi kerak"""
        # Boshqa student uchun ham ariza yaratamiz
        EnrollmentRequest.objects.create(student=self.other_student, group=self.group)

        # birinchi student sifatida tizimga kiramiz
        self.client.force_authenticate(user=self.student)
        url = reverse("enrollment-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Jami 2 ta ariza bor, lekin student faqat 1 tasini (o'zinikini) ko'rishi kerak
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["student"], self.student.id)