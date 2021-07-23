import json


class PeopleRepository(object):

    def __init__(self, client):
        self.client = client

    def _execute(self, query, variables={}):
        return self.client.txn(read_only=True).query(query, variables=variables)

    def get_all(self):

        query = """
            {
                people(func: has(name)) {
                    name
                }
            }
        """

        res = self._execute(query)
        return json.loads(res.json)['people']

    def get_friends(self, name):

        query = """
            query people($a: string) {
                people(func: alloftext(name, $a))
                {
                    knows {
                            name
                    }
                    ~knows {
                        name
                    }
                }
            }
        """

        res = self._execute(query, variables={'$a': name})
        return json.loads(res.json)['people'][0]
