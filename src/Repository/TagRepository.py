import csv
from Entity.Tag import Tag
from Service.ElasticService import ElasticService
from pprint import pprint


class TagRepository:
    index_name = 'tags'

    def get_data_from_file(self, file_path: str):
        tag_file = open(file_path, 'r')
        tag_rows = csv.DictReader(tag_file)
        tags = {}
        i = 0
        for tag_row in tag_rows:
            tag = Tag(i, int(tag_row['userId']), int(tag_row['movieId']), tag_row['tag'], int(tag_row['timestamp']))
            tags[i] = tag
            i += 1

        return tags

    def get_es_index_data(self, tags: dict, movies: dict):
        for tag_id, tag in tags.items():
            tag_dict = tag.__dict__
            tag_dict['movie_title'] = movies[tag.movie_id].title
            print(self.index_name + ' doc with id: ' + repr(tag.id) + ' imported')

            yield tag_dict

    def create_es_index_with_data(self, tags: dict, movies: dict):
        request_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "user_id": {"type": "keyword"},
                    "movie_id": {"type": "keyword"},
                    "movie_title": {"type": "search_as_you_type"},
                    "tag": {"type": "search_as_you_type"},
                    "timestamp": {"type": "date", "format": "epoch_second"}
                }
            }
        }
        data = self.get_es_index_data(tags=tags, movies=movies)
        ElasticService.create_index_with_data(data=data, index=self.index_name, request_body=request_body)
