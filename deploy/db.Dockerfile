FROM dgraph/standalone:v20.03.0

EXPOSE 8000
EXPOSE 8080
EXPOSE 9080

COPY deploy/run-db.sh /
COPY deploy/populate-db.sh /
CMD ["sh", "/run-db.sh"]