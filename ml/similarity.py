# Function that takes in movie title as input and outputs most similar movies
# from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
# cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(title, cosine_sim):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]
    track_indices = [i[0] for i in sim_scores]

    return data2['title'].iloc[track_indices]
