from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.com",
            first_name="Администратор",
            last_name="Администраторов",
            tg_chat_id="1271362249",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password("123")
        user.save()
