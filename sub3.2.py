import csv
import json

movies = []
genres = []

with open('datasets/movies.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if(row['genres']!='(no genres listed)'):
            movies.append(row)
            splt = row['genres'].split("|")
            for genre in splt:
                if(not genre in genres):
                    genres.append(genre)

# print(genres)

ratings = []
with open('datasets/ratings.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ratings.append(row)

users = []
genresDict = { x:0 for x in genres }

temp = {'userId':ratings[0]['userId']}
temp.update(genresDict)
users.append(temp)
movieCounter = 0 
cur_user_id = users[0]['userId']

for row in ratings:
    if(row['userId']!=cur_user_id):
        # print('1.-----------------row id is different than cur_user_id')
        for genre in genresDict: 
            users[-1][genre] = round(users[-1][genre]/movieCounter, 6)
        movieCounter = 1
        temp = {'userId':row['userId']}
        temp.update(genresDict)
        users.append(temp)
        cur_user_id = row['userId']
    else:
        # print('2.-----------------row id is the same as cur_user_id')
        movieCounter += 1

    for movie in movies:
        if(movie['movieId'] ==  row['movieId']):
            movieGenres = movie['genres'].split('|')
            for genre in genres:
                if(genre in movieGenres):
                    users[-1][genre] += float(row['rating'])
                else:
                    users[-1][genre] += 0

for genre in genresDict:
    users[-1][genre] = round(users[-1][genre]/movieCounter, 6)

my_json_string = json.dumps(users)
with open('tempdata.json','w',encoding='utf8') as f:
    f.write(my_json_string)
