from django.db.models import Manager


class AuthorSoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
