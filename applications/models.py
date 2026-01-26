from django.db import models

from authentication.models import User

# Create your models here.
class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=100)
    program_name = models.CharField(max_length=50) 
    study_mode = models.CharField(max_length=20, choices=[('Online','Online'),('On-Campus','On-Campus')]) 
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'Student'}, related_name='applications_student')
    status = models.CharField(max_length=10, choices=[('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')], default='Pending')
    subject = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)

    def __str__(self):
        return f"{self.university_name} - {self.subject}"