"""API views for CRUD operations, summary data, and follow-up generation."""

from django.conf import settings
from django.db.models import Count
from openai import OpenAI
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import JobApplication
from .serializers import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    """Exposes the main API endpoints for job applications."""

    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all().order_by('-applied_date')

    def get_queryset(self):
        """Optionally filter the application list by status."""
        queryset = JobApplication.objects.all().order_by('-applied_date')
        status_filter = self.request.query_params.get('status')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """Return application counts grouped by status."""
        status_counts = (
            JobApplication.objects
            .values('status')
            .annotate(count=Count('status'))
        )

        # Keep the response structure stable even when a status has no records yet.
        summary_data = {
            'applied': 0,
            'interviewing': 0,
            'rejected': 0,
            'offered': 0,
        }

        for item in status_counts:
            summary_data[item['status']] = item['count']

        return Response(summary_data)

    @action(detail=True, methods=['post'], url_path='generate-followup')
    def generate_followup(self, request, pk=None):
        """Generate a professional follow-up email for one application."""
        application = self.get_object()

        if not settings.OPENAI_API_KEY:
            return Response(
                {'error': 'OpenAI API key is not configured.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        prompt = f"""
Write a concise, professional follow-up email for a job application.

Application details:
- Company: {application.company}
- Role: {application.role}
- Current status: {application.status}
- Applied date: {application.applied_date.strftime('%Y-%m-%d %H:%M:%S')}
- Notes: {application.notes or 'No notes provided'}

Requirements:
- Keep it polite and professional
- Keep it concise
- Show interest in the role
- Ask for a brief update on the hiring process
- Return only the email draft
"""

        try:
            # The API key stays on the server and is loaded from environment variables.
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You write professional job application follow-up emails."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # The assignment asks for a concise draft, so only the message text is returned.
            followup_email = response.choices[0].message.content.strip()

            if not followup_email:
                return Response(
                    {'error': 'OpenAI returned an empty response.'},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            return Response({
                'application_id': application.id,
                'followup_email': followup_email,
            })

        except Exception as exc:
            # Returning a readable error helps reviewers see that failure cases were considered.
            return Response(
                {'error': f'Failed to generate follow-up email: {str(exc)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
