import json  
import hdbscan

with open('tempdata.json',encoding='utf8') as f:
    users = json.load(f)

genres = []
for genre in users[0]:
    if(not genre in genres and genre != 'userId'):
        genres.append(genre)

usersMatrix = []
# tempVector = []
for item in users:
    tempVector = []
    for genre in genres:
        tempVector.append(item[genre])
    usersMatrix.append(tempVector)

clusterer = hdbscan.HDBSCAN()
clusterer.fit(usersMatrix)
print(clusterer.labels_)
# for item in usersMatrix:
#     print(item)