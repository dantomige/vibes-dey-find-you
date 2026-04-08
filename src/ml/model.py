"""
Two-tower model.
Encoding of user profile + user query. Encoding of song metadata + audio feature (stored in long term after training to find this). Cosine similarity and return top k songs

Cross attention model.
Feed everything into a transformer : [query tokens] + [user features] + [song metadata] + [audio features]
Allows for more complex interaction.


* Make sure to use the same encoder when it comes to vectorizing readable text (queries, titles, genres)

"""
