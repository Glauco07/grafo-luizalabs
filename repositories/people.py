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
        friends = json.loads(res.json)['people']
        
        return friends[0] if len(friends) > 0 else None

    def get_uids(self, names):

        uids = []

        for name in names:

            query = """
                query people($a: string) {
                    people(func: eq(name, $a))
                    {
                        uid
                    }
                }
            """

            res = self._execute(query, variables={'$a': name})
            uid = json.loads(res.json)['people']

            if len(uid) > 0:
                uids.append(uid[0])

        return uids if len(uids) > 0 else None

    def add_people(self, key, uids):
        
        mutation = {
            'name': key,
            'knows': uids
        }

        self.client.txn().mutate(set_obj=mutation) # ver se inserir está funcionando. Lembrar de trocar localhost para db
