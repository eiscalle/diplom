from datetime import datetime
from django.contrib.auth.backends import ModelBackend
from portal.user.models import PortalUser


class FabricBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        UserModel = PortalUser
        fabricUser = UserModel.check_fabric_auth(username, password)
        if fabricUser is False:
            return None
        try:
            user = UserModel.objects.get(work_email=username)
            user.first_name = fabricUser['firstname']
            user.last_name = fabricUser['lastname']
            user.placement_date = datetime.strptime(fabricUser['created_on'], "%Y-%m-%dT%H:%M:%SZ")
        except UserModel.DoesNotExist:
            user = UserModel(
                work_email=fabricUser['mail'],
                first_name=fabricUser['firstname'],
                last_name=fabricUser['lastname'],
                placement_date=datetime.strptime(fabricUser['created_on'], "%Y-%m-%dT%H:%M:%SZ")
            )
        user.set_password(password)
        user.save()
        return user