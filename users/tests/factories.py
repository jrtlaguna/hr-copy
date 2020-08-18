import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = "testuserpassword"
    first_name = factory.Sequence(lambda n: f"Foo{n}")
    last_name = "Bar"
    email = factory.Sequence(lambda n: f"person{n}@gmail.com")
