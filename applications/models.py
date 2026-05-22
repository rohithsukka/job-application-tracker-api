"""Database models for the job application tracker."""

from django.db import models


class JobApplication(models.Model):
    """Stores the details of a single job application."""

    # These fixed values keep the API aligned with the assignment requirement.
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('rejected', 'Rejected'),
        ('offered', 'Offered'),
    ]

    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied',
    )
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        """Show a readable label in the Django admin and shell."""
        return f"{self.company} - {self.role}"
