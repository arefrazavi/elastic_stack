import csv
from Entity.Rating import Rating
from Service.ElasticService import ElasticService


class RatingRepository:
    index_name = 'ratings'

    def get_data_from_file(self, file_path):
        rating_file = open(file_path, 'r')
        rating_rows = csv.DictReader(rating_file)
        ratings = {}
        i = 0
        for rating_row in rating_rows:
            rating = Rating(i, int(rating_row['userId']), int(rating_row['movieId']), float(rating_row['rating']), int(rating_row['timestamp']))
            ratings[i] = rating
            i += 1

        return ratings

    def get_es_index_data(self, ratings: dict, movies: dict):
        for rating_id, rating in ratings.items():
            rating_dict = rating.__dict__
            rating_dict['movie_title'] = movies[rating.movie_id].title
            print(self.index_name + ' doc with id: ' + repr(rating.id) + ' imported')

            yield rating_dict

    def create_es_index_with_data(self, ratings: dict, movies: dict):
        request_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "user_id": {"type": "keyword"},
                    "movie_id": {"type": "keyword"},
                    "movie_title": {"type": "search_as_you_type"},
                    "rating": {"type": "float"},
                    "timestamp": {"type": "date", "format": "epoch_second"}
                }
            }
        }
        data = self.get_es_index_data(ratings=ratings, movies=movies)
        ElasticService.create_index_with_data(data=data, index=self.index_name, request_body=request_body)

