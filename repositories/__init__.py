from .people import PeopleRepository


def create_people_repository(client):
    return PeopleRepository(client)
