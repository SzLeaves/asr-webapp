from import_export import resources

from users.models import EmailVerifyRecord
from users.models import UserProfile


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class VerifyRecordResource(resources.ModelResource):
    class Meta:
        model = EmailVerifyRecord
