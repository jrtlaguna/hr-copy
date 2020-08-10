import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = "testuserpassword"
    first_name = "Foo"
    last_name = "Bar"
    email = "testuser@gmail.com"
