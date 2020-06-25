from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    middle_name = models.CharField('Middle Name', max_length=150, null=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Employee(models.Model):

    MALE = 1
    FEMALE = 2
    OTHER = 3

    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, 'Other')
    )

    user = models.OneToOneField(
        'users.User',
        verbose_name='User',
        related_name='employee',
        on_delete=models.CASCADE
    )


    gender = models.IntegerField('Gender', choices=GENDER_CHOICES,)
    date_of_birth = models.DateField("Date of Birth", auto_now_add=False,)
    date_started = models.DateField("Date Started", auto_now_add=False,)
    is_active = models.BooleanField("Is active", default=True)
    nickname = models.CharField("Nickname", max_length=100, null=True, blank=True)

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.email

class EmergencyContact(models.Model):

    name = models.CharField("Name", max_length=100)
    contact_number = models.CharField('Contact No.', max_length=100)
    employee = models.ForeignKey(
        "users.employee",
        verbose_name="Employee",
        related_name="emergency_contact",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Emercency Contact'
        verbose_name_plural = 'Emergency Contacts'

    def __str__(self):
        return self.name
        

class Education(models.Model):

    school = models.CharField("School", max_length=100,)
    level = models.CharField("Level", max_length=100,)
    degree = models.CharField("Degree", max_length=100,)
    year_graduated = models.CharField("Year Graduated", max_length=50,)

    employee = models.ForeignKey(
        'users.employee',
        verbose_name="Employee",
        related_name='history',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.school

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = "Education"


class WorkHistory(models.Model):

    company = models.CharField("Company", max_length=100,)
    position = models.CharField("Position", max_length=100,)
    employee = models.ForeignKey(
        'users.employee',
        verbose_name="Employee",
        related_name='education',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = 'Work History'
        verbose_name_plural = 'Work History'

