from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

ECOLES = (
    ("aviationMilitaire", "Ecole spécialisé dans l'avation militaire"),
    ("aviationCivile", "Ecole spécialisé dans l'avation civile"),
    ("aviationLoisirSportif", "Ecole spécialisé dans l'avation loisir et sportive"),
    )
HORAIRES = (
    ("8h", "8h"),
    ("10h", "10h"),
    ("12h", "12h"),
    ("14h", "14h"),
    ("16h", "16h"),
    ("18h", "18h"),
    ("20h", "20h"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ecoles = models.CharField(max_length=50, choices=ECOLES, default="aviationCivile")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=HORAIRES, default="10h")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"reservation de l'école : {self.ecoles}, par {self.user} | jour: {self.day} | heure: {self.time}"
