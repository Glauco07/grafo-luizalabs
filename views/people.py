import json


class PeopleViews(object):

    def __init__(self, service, router):
        self.service = service
        self.router = router
        self._create_routes()

    def _create_routes(self):

        @self.router.route('/', methods=['GET'])
        def home():
            return '', 200

        @self.router.route('/people', methods=['GET'])
        def get_all():

            people = self.service.get_all()
            return json.dumps(people), 200

        @self.router.route('/people/<name>')
        def get_person_friends(name):

            if name == '':
                return json.dumps({}), 400

            friends = self.service.get_friends(name)
            return json.dumps(friends), 200
