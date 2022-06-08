import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def get_recommendation(isbn):
    
    ratings = pd.read_csv("./data/ratings.csv", encoding='latin-1', low_memory=False)
    books = pd.read_csv("./data/books.csv", encoding='latin-1', low_memory=False)
    users = pd.read_csv("./data/users.csv", encoding='latin-1', low_memory=False)

    combine_book_rating = pd.merge(ratings, books, on='ISBN')

    # build knn
    user_rating = combine_book_rating.drop_duplicates(['User-ID', 'Book-Title'])
    user_rating_pivot = user_rating.pivot(index = 'ISBN', columns = 'User-ID', values = 'Book-Rating').fillna(0)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(user_rating_pivot)

    query_index = user_rating_pivot.index.tolist().index(isbn)
    distances, indices = model_knn.kneighbors(user_rating_pivot.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 5)
    user_rating_pivot.index[query_index]

    result = []
    for i in range(0, len(distances.flatten())):
        book = user_rating_pivot.index[indices.flatten()[i]]
        result.append(book)
    return result