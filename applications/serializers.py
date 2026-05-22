"""Serializers for converting model data to and from JSON."""

from rest_framework import serializers

from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    """Validates API input and exposes job applications as JSON."""

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'company',
            'role',
            'status',
            'applied_date',
            'notes',
        ]
        # These values are created by the system and should not be supplied by clients.
        read_only_fields = ['id', 'applied_date']
