import factory
from faker import Faker

from ..models import User, ServiceArea


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')
    phone_number = 111111


class ServiceAreaFactory(factory.DjangoModelFactory):

    class Meta:
        model = ServiceArea

    created_by = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    price = factory.Faker('pyfloat')

    @factory.lazy_attribute
    def area(self):
        faker = Faker()
        # In GeoJSON, the correct coordinate order is longitude, latitude
        prefix = suffix = (float(faker.longitude()), float(faker.latitude()))
        coords = [(float(faker.longitude()), float(faker.latitude())) for _ in range(2)]
        coords.append(suffix)
        coords.insert(0, prefix)

        data = {
            "type": "polygon",
            "coordinates": [coords]
        }

        return data