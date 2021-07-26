import requests
import time


def create_schema():
    url = 'http://localhost:8080/alter?runInBackground=true'

    payload = '''
    name: string @index(fulltext) .
    knows: [uid] @reverse .
    '''

    requests.post(url, data=payload)


def populate_db():
    url = 'http://localhost:8080/mutate?commitNow=true'
    headers = {'Content-Type': 'application/json'}
    payload = '{"set":[{"name": "Carlos","knows":[{"name": "Ana","knows":[{"name": "Maria"},{"name": "João","knows":[{"name": "Luiza"}]}]}]}]}'.encode('utf-8')

    requests.post(url, headers=headers, data=payload)
    
    r = requests.post('http://localhost:5000/people', json={"Vinicius": ["Maria", "Ana"]})
    print(r.json())


def run():
    create_schema()
    time.sleep(5)
    populate_db()


if __name__ == '__main__':
    run()
