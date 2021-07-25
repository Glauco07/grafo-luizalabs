import json

from flask import request


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

        @self.router.route('/people/<name>', methods=['GET'])
        def get_person_friends(name):

            if name == '':
                return json.dumps({}), 400

            friends = self.service.get_friends(name)

            return json.dumps(friends), 200

        @self.router.route('/people/<name>/level2', methods=['GET'])
        def get_second_level(name):
            unknown_people = self.service.get_unknown_people(name)

            return json.dumps(unknown_people), 200

        @self.router.route('/people', methods=['POST'])
        def add_people():
            # recebe um dict cuja key é o nome da pessoa a ser inserida, e o value é uma lista de nomes que essa pessoa conhece

            payload = request.json
            if payload is None:
                message = json.dumps({'message': 'The body of the request is a not valid JSON.'})
                return message, 400

            result = self.service.add_people(payload) 
            if result is None:
                return json.dumps({'message': 'Could not insert one or more people.'}), 400

            return json.dumps({'message': 'All people inserted.'}), 201
