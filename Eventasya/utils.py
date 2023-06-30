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
