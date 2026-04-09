from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    try:
        if action == "post_add":  # triggered after user added
            for user_id in pk_set:
                user = User.objects.get(pk=user_id)

                send_mail(
                    f"RSVP Confirmation for {instance.name}",
                    f"Hi {user.username}, You have successfully RSVP'd to the event: {instance.name}. Location: {instance.location}. Date: {instance.date}.Thank you for joining!- Event Team",
                    "settings.EMAIL_HOST_USER",
                    [user.email],
                    fail_silently=False,
                    )
                
    except Exception as e:
        print("❌ Email failed:", e)
            

            


