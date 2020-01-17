import csv
import json

movies = []
genres = []
genresPop = {}
with open('datasets/movies.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if(row['genres']!='(no genres listed)'):
            movies.append(row)
            splt = row['genres'].split("|")
            for genre in splt:
                if(not genre in genres):
                    genres.append(genre)
                    genresPop.update({genre:1})
                else:
                    genresPop[genre] +=1

print(genres)
print('Genres population:',genresPop)
# print(movies)

ratings = []
with open('datasets/ratings.csv',encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ratings.append(row)

movieGenresNotIncluded = []
users = []
genresDict = { x:0 for x in genres }
# print('genresDict:',genresDict)
temp = {'userId':ratings[0]['userId']}
temp.update(genresDict)
users.append(temp)
# print('users init:',users)
# print(users)
movieCounter = 1 
cur_user_id = users[0]['userId']
# print('cur_user_id init:',cur_user_id)
for row in ratings:
    # print('---------------------------------')
    # print('row:',row)
    if(row['userId']!=cur_user_id):
        # print('1.-----------------row id is different than cur_user_id')
        # print('movie counter = ',movieCounter)
        # print('users[-1] before:',users[-1])
        # for genre in genresDict: -=-=-=-=-=-
            # print('genre:',genre)
            # users[-1][genre] = users[-1][genre]/movieCounter -=-=-=-=
            # users[-1][genre] = round(users[-1][genre], 3) -=-=-=-=-
        # print('users[-1] after:',users[-1])
        movieCounter = 0
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
                movieGenresNotIncluded = []
                #assumption that 2.5 is the indifferent ranking ---
                for genre in genres:
                    if(not genre in movieGenres):
                        movieGenresNotIncluded.append(genre)
                # print('not included:',movieGenresNotIncluded)
                for genreName in movieGenresNotIncluded:
                    users[-1][genreName] += 2.5
                #assumption end ----------------------------------
                for genreName in movieGenres:
                    users[-1][genreName] += float(row['rating'])
                # print(users[-1])
# for genre in genresDict: -=-=-=-
    # print('genre:',genre)
    # users[-1][genre] = users[-1][genre]/movieCounter -=-=-=
    # users[-1][genre] = round(users[-1][genre], 2) -=-=-=-=

my_json_string = json.dumps(users)
with open('tempdata.json','w',encoding='utf8') as f:
    f.write(my_json_string)

# usersMatrix = []
# # tempVector = []
# for item in users:
#     tempVector = []
#     for genre in genresDict:
#         tempVector.append(item[genre])
#     usersMatrix.append(vector)

# for item in usersMatrix:
#     print(item)


