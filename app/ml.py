import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import BlogPost


def combined_feature(row):
    return row['title'] + " " + row['content']


df = pd.DataFrame(list(BlogPost.objects.all().values()))
features = ['title', 'content']
for feature in features:
    df[feature] = df[feature].fillna('')

df["combined_features"] = df.apply(combined_feature, axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)


def get_id_from_index(df, index):
    return df[df.index == index]["id"].values[0]


def get_index_from_id(df, id):
    return df[df.id == id].index.values[0]


def get_recommendation_for_blog(blog_id):

    id = get_index_from_id(df, blog_id)

    similar_blog = list(enumerate(cosine_sim[id]))\

    sorted_similar_blog = sorted(
        similar_blog, key=lambda x: x[1], reverse=True)

    i = 1
    blog_ids = []
    for blog in sorted_similar_blog[1:]:
       
        blog_ids.append(get_id_from_index(df, blog[0]))
        i = i + 1
        if i > 15:
            break

    return blog_ids
