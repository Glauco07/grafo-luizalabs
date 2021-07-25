class PeopleService(object):
    
    def __init__(self, people_repository):
        self.repository = people_repository

    def get_all(self):

        people = self.repository.get_all()
        return [person['name'] for person in people]

    def get_friends(self, name):

        raw_friends = self.repository.get_friends(name)

        if raw_friends is None:
            return None
    
        people = [
            *raw_friends.get('knows', []),
            *raw_friends.get('~knows', [])
        ]

        return [person['name'] for person in people]

    def get_unknown_people(self, name):

        people = self.repository.get_friends(name)

        unkown_people = []

        for person in people:
            friends = self.repository.get_friends(person)
            if friends is None:
                return None

            for friend in friends:
                if friend not in people and friend != name:
                    unkown_people.append(friend)

        return unkown_people

    def add_people(self, payload):

        people = self.get_all()

        for key, values in payload.items():
            for value in values:
                if value not in people:
                    return None
            uids = self.repository.get_uids(values)
            self.repository.add_people(key, uids)
            return True
