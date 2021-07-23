from .people import PeopleService


def create_people_service(people_repository):
    return PeopleService(people_repository)
