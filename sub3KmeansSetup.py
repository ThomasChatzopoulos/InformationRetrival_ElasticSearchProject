import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

import plotly.express as px

ratings = pd.read_csv('datasets/ratings.csv')

users = ratings.groupby('userId', as_index=False)['rating'].mean()

wcss = []
for i in range(1, 10):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(np.array(users['rating']).reshape(-1,1))
    wcss.append(kmeans.inertia_)

fig = px.line(x=range(1, 10),y= wcss,)
fig.update_layout(
    title="Within Cluster Sum of Squares (WCSS) line",
    xaxis_title="Number of clusters",
    yaxis_title="Wcss",
    font=dict(
        family="Courier New, monospace",
        size=30,
        color="#7f7f7f"
    )
)
fig.show()