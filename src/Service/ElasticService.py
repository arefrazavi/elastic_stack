import elasticsearch
from elasticsearch import helpers
import collections

class ElasticService:

    @staticmethod
    def create_index_with_data(data, index: str, request_body: dict):
        es = elasticsearch.Elasticsearch()

        # Ignore 404 error when index doesn't exist.
        es.indices.delete(index=index, ignore=404)

        # Ignore 400 error caused by IndexAlreadyExistsException when creating an index
        es.indices.create(index=index, body=request_body, ignore=400)

        # Bulk add documents
        collections.deque(helpers.parallel_bulk(client=es, actions=data, index=index))

        # Refresh Index
        es.indices.refresh()

