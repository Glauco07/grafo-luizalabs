import pydgraph

from flask import Flask

from repositories import create_people_repository
from services import create_people_service
from views import create_people_views


app = Flask(__name__)

db_stub = pydgraph.DgraphClientStub('db:9080')
db_connection = pydgraph.DgraphClient(db_stub)

repository = create_people_repository(db_connection)
service = create_people_service(repository)
view = create_people_views(service, app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
