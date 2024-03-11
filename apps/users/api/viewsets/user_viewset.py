
from apps.base.viewsets.viewsets_generics import GenericReadOnlyViewset
from apps.users.api.serializers.user_serializers import UserReadOnlySerializer, UserSerializer



class UserModelViewset(GenericReadOnlyViewset):
    serializer_class = UserSerializer
    read_only_serializer = UserReadOnlySerializer
    search_fields = [
        "username",
        "first_name",
        "last_name",
    ]