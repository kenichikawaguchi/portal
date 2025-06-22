from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_signed_up)
def send_admin_notification(request, user, **kwargs):
    subject = '新しいユーザーが登録されました'
    message = f'{user.username}さんが新しく登録されました。'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_ADMIN]
    send_mail(subject, message, from_email, recipient_list)

