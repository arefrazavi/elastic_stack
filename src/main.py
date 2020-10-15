from Repository.MovieRepository import MovieRepository
from Repository.RatingRepository import RatingRepository
from Repository.TagRepository import TagRepository
import pprint
import os

base_path = os.getcwd()

# Retrieve indices data from dataset.
movies_file_path = base_path + '/../dataset/ml-latest-small/movies.csv'
movie_repo = MovieRepository()
movies = movie_repo.get_data_from_file(movies_file_path)

ratings_file_path = base_path + '/../dataset/ml-latest-small/ratings.csv'
rating_repo = RatingRepository()
ratings = rating_repo.get_data_from_file(ratings_file_path)

tags_file_path = base_path + '/../dataset/ml-latest-small/tags.csv'
tag_repo = TagRepository()
tags = tag_repo.get_data_from_file(tags_file_path)

# Create ES indices.
movie_repo.create_es_index_with_data(movies)
print('\n-----------\n')
rating_repo.create_es_index_with_data(ratings, movies)
print('\n------------\n')
tag_repo.create_es_index_with_data(tags, movies)

# Iterate over a dictionary.
# for tag_id, tag in tags.items():
#     # Cast object into dictionary
#     movie_dict = tag.__dict__
#     pprint.pprint(movie_dict)
#     print('\n')
