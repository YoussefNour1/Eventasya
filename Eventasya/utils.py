import requests
from django.core.mail import get_connection, EmailMessage

from Eventasya import settings


def send_email(subject, message, email_to):
    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        fail_silently=False
    )
    connection.open()

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_FROM,
        to=email_to,
        connection=connection
    )

    email.content_subtype = "html"
    email.send()
    connection.close()


def send_http_email(subject, message, email_to):
    # Set up the email service provider's API endpoint and headers
    api_endpoint = 'https://api.brevo.com/v3/smtp/email'
    api_key = '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'
    headers = {'Content-Type': 'application/json', 'api-key': f'{api_key}'}
    body = {
        "sender": {
            "name": "Eventasya Platform",
            "email": "eventasyaplatform@gmail.com"
        },
        "to": [
            {
                "email": email_to,
            }
        ],
        "htmlContent": message,
        "subject": subject
    }

    try:
        # Send the email request
        response = requests.post(api_endpoint, headers=headers, json=body)

        if response.status_code == 201:
            print('Email sent successfully')
        else:
            print(f'Failed to send email. Error: {response.text}, {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to send email. Error: {str(e)}')