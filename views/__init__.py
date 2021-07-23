from .people import PeopleViews


def create_people_views(service, router):
    return PeopleViews(service, router)
