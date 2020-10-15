import csv
import re
from Entity.Movie import Movie
from Service.ElasticService import ElasticService


class MovieRepository:
    index_name = 'movies'

    def get_data_from_file(self, file_path):
        movie_file = open(file_path, 'r')
        movie_rows = csv.DictReader(movie_file)
        movies = {}
        for movie_row in movie_rows:
            movie_title = re.sub(" \(.*\)$", "", re.sub('"', '', movie_row['title']))
            movie_release_date = movie_row['title'][-5:-1]
            if (not movie_release_date.isdigit()):
                movie_release_date = "2016"
            movie_genre = movie_row['genres'].split('|')
            movie_id = int(movie_row['movieId'])
            movie = Movie(movie_id, movie_title, movie_genre, movie_release_date)
            movies[movie.id] = movie

        return movies

    def get_es_index_data(self, movies: dict):
        for movie_id, movie in movies.items():
            movie_dict = movie.__dict__
            print(self.index_name + ' doc with id: ' + repr(movie.id) + ' imported')

            yield movie_dict

    def create_es_index_with_data(self, movies: dict):
        request_body = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    # genre is an array of "search_as_you_type" type values
                    "genre": {"type": "search_as_you_type"},
                    "title": {"type": "search_as_you_type"},
                    "release_date": {"type": "date", "format": "year"}
                }
            }
        }
        data = self.get_es_index_data(movies)
        ElasticService.create_index_with_data(data=data, index=self.index_name, request_body=request_body)
