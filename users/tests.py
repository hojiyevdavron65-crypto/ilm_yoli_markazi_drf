from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    """User modelini sinash"""

    def test_default_role_is_student(self):
        """role ko'rsatilmasa, avtomatik student bo'lishi kerak"""
        user = User.objects.create_user(username="oddiy_user", password="test12345")
        self.assertEqual(user.role, User.Role.STUDENT)

    def test_create_admin_user(self):
        """Admin user to'g'ri yaratilishi kerak"""
        admin = User.objects.create_user(
            username="admin_test",
            password="Admin12345!",
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )
        self.assertEqual(admin.role, User.Role.ADMIN)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_teacher_user(self):
        """Ustoz user to'g'ri yaratilishi kerak"""
        teacher = User.objects.create_user(
            username="teacher_test",
            password="Teacher12345!",
            role=User.Role.TEACHER,
        )
        self.assertEqual(teacher.role, User.Role.TEACHER)
        self.assertFalse(teacher.is_staff)

    def test_create_student_user(self):
        """O'quvchi user to'g'ri yaratilishi kerak"""
        student = User.objects.create_user(
            username="student_test",
            password="Student12345!",
            role=User.Role.STUDENT,
        )
        self.assertEqual(student.role, User.Role.STUDENT)
        self.assertFalse(student.is_staff)

    def test_password_is_hashed(self):
        """Parol ochiq matn holida saqlanmasligi kerak"""
        user = User.objects.create_user(username="testuser", password="test12345")
        self.assertNotEqual(user.password, "test12345")
        self.assertTrue(user.check_password("test12345"))

    def test_str_representation(self):
        """__str__ metodi to'g'ri formatda chiqishi kerak"""
        user = User.objects.create_user(
            username="testuser2", password="test12345", role=User.Role.TEACHER
        )
        self.assertEqual(str(user), "testuser2 (Ustoz)")

    def test_username_must_be_unique(self):
        """Bir xil username bilan ikkinchi user yaratib bo'lmasligi kerak"""
        User.objects.create_user(username="unique_user", password="test12345")
        with self.assertRaises(Exception):
            User.objects.create_user(username="unique_user", password="boshqa12345")