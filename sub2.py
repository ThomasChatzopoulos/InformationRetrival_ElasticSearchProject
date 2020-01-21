import csv
import multiprocessing as mp
from datetime import time

import pandas as pd

from elasticsearch import helpers, Elasticsearch
# import multiprocessing

# Elastic search must be active
# If the input is 'q' the loop is terminated

es = Elasticsearch()
# print("write your query:")
# query = input()
# print("write your id:")
# user_id_input = int(input())  # to user id poy plhktrologei o xrhsths

# temp_score_array = []  # gia ka8e ypopinaka [x,y,z]: X: baumologia elasticsearch, y: baumologia xrhsth, z: mo baumologiwn tainias
# temp_id_array = []  # gia ka8e tainia sto for loop kratame kai to id
# temp_movies_mo_rating_array = []  # gia mo kaue tainiaw apo xrhstes [x,y,z]: x: id tainias, y: a8roisma baumologiwn, z: plh80s xrhstwn
# score_array = []  # pinakas telikhs ba8mologias
# mo = []  # mesos oros [x,y]: X: id tainias, y: mo
# ratings_file = []

# with open('datasets/ratings.csv', mode='r') as csv_file:  # diabasma arxeiou ratings
#     print("Process: Reading File ...")
#     temp_ratings_file = csv.reader(csv_file)
#     # print(temp_ratings_file)
#     flag = 0
#     for row in temp_ratings_file:
#         if flag != 0:
#             ratings_file.append(row)
#         else:
#             flag = 1
#     #   print(row)
#     # print(ratings_file)

ratings = pd.read_csv('datasets/ratings.csv')

# # temp_movies_mo_rating_array.append([ratings_file[0][1], ratings_file[0][2], 1])
# # print(temp_movies_mo_rating_array)
# print("Process: Reading File OK!")
# print("Process: Movie MO calculation from file...")
# for row in range(len(ratings_file)):  # gia dhmiourgia pinaka me/gia mo tainiwn apo xrhstes
#     get_in_if = 0
#     for movie in temp_movies_mo_rating_array:  # gia ta stoixeia pou uparxoun mesa,
#         # print("movie", movie)
#         if int(ratings_file[row][1]) == int(movie[0]):  # an uparxei h tainia ston pinaka
#             temp_movies_mo_rating_array[temp_movies_mo_rating_array.index(movie)] = [int(ratings_file[row][1]), float(movie[1]) + float(ratings_file[row][2]), int(movie[2] + 1)]
#             get_in_if = 1
#             continue
#     if get_in_if == 0:  # an den uparxei prοs8ese thn
#         temp_movies_mo_rating_array.append([int(ratings_file[row][1]), float(ratings_file[row][2]), int(1)])
#         # print("movie", movie)
# #     print("temp_movies_mo_rating_array ", temp_movies_mo_rating_array)


# print("len", len(temp_movies_mo_rating_array))
# # print(temp_movies_mo_rating_array)
# print("Process: Movie MO calculation from file OK!")
# print("Process: New MO movie matric calculation ...")
# for movie in range(len(temp_movies_mo_rating_array)):  # dhmiourgia pinaka me mo
#     # print("movie[0]:", temp_movies_mo_rating_array[movie][0])
#     # print("movie[1]:", temp_movies_mo_rating_array[movie][1])
#     # print("movie[2]:", temp_movies_mo_rating_array[movie][2])
#     MO = temp_movies_mo_rating_array[movie][1] / temp_movies_mo_rating_array[movie][2]  # mesos oros tainias
#     # print("MO:      ", MO)
#     mo.append([int(temp_movies_mo_rating_array[movie][0]), float(MO)])  # id_tainias, mo
#     # print(mo)
# print("Process: New MO movie matric calculation OK!")

movies_mo = ratings.groupby('movieId', as_index=False)['rating'].mean()

# while query != 'q':
    # results = es.search(index="movies", body={"query": {"match": {'title': query}}})
    # # print("test", ratings_file[50][0])
    # # to for loop: gia na paroume apo to arxeio result to score ths tainias id kai na broume thn triada ba8mologiwn
    # print("Process: Optimize to user ...")
    # for row in range(len(ratings_file)):  # gia to arxiko arxeio ba8mologiwn
    #     user_id_value = int(ratings_file[row][0])  #id xrhsth gia elegxo
    #     # print("user_id_value:", user_id_value)
    #     if user_id_input == user_id_value:  # an o xrhsths exei baumologhsei kapoia tainia genika (an uparxei to id tou user)
    #         for x in range(len(results["hits"]["hits"])):
    #             if results["hits"]["hits"][x]["_source"]["movieId"] == ratings_file[row][1]:  # an o xrhsths exei baumologhsei thn sugkekrimenh tainia pou emfanizetai sta apotelesmata
    #                 for k in range(len(mo)):
    #                     if mo[k][0] == ratings_file[row][1]:  # an uparxei, 8a uparxei mia fora
    #                         temp_score_array.append([float(results["hits"]["hits"][x]["_score"]), float(ratings_file[row][2]), float(mo[k][1])])  # 8a ginei to polu mia eggrafh
    #                         temp_id_array.append(mo[k][0])  # opote ginetai pros8hkh mias eggrafhs, 8a ginetai pros8hkh sthn idia 8esh kai to id ths tainias
    #                         continue
    #             else:  # an o xrhsths den exei baumologhsei thn sugkekrimenh tainia pou emfanizetai sta apotelesmata
    #                 for k in range(len(mo)):
    #                     # movie_id_value = int(ratings_file[row][1])
    #                     # print("movie_id_value:", movie_id_value)
    #                     if mo[k][0] == int(ratings_file[row][1]):  # an uparxei 8a uparxei mia fora
    #                         temp_score_array.append([float(results["hits"]["hits"][x]["_score"]), float(mo[k][1])])  # 8a ginei to polu mia eggrafh
    #                         temp_id_array.append(mo[k][0])  # opote ginetai pros8hkh mias eggrafhs, 8a ginetai pros8hkh sthn idia 8esh kai to id ths tainias
    #                         continue
    #         # print("len_results:", temp_score_array)

    # # print("temp_score_array:", temp_score_array[0][0])
    # max_element = temp_score_array[0][0]  # gia  megisth timh metrikhs elasticsearch
    # position = temp_id_array[0]  # 8esh max stoixeiou
    # print("Process: New MO movie matric calculation OK!")
    # print("Process: Finding optimal order of preference ...")
    # for index in range(len(temp_score_array)):  # euresh timhs kai 8eshs megisths timhs mo gia kanonikopoihsh
    #     if temp_score_array[index][0] > max_element:
    #         max_element = temp_score_array[index][0]
    #         position = temp_id_array[index]

    # for index in range(len(temp_score_array)):  # kanonikopoihsh timwn
    #     temp_score_array[index][0] = temp_score_array[index][0] / max_element
    #     temp_score_array[index][1] = temp_score_array[index][1] / 5.0
    #     if len(temp_score_array[index]) > 2:  # se kapoia stoixeia uparxoun 2, se alla 3 times
    #         temp_score_array[index][2] = temp_score_array[index][2] / 5.0

    # for index in range(len(temp_score_array)):  # dhmiourgia neas metrikhs/euresh neou mo
    #     summary = 0
    #     for value in range(len(temp_score_array[index])):
    #         summary += temp_score_array[index][value]
    #     mo[index][1] = (summary / len(temp_score_array[index]))  # mesos oros dia8esimwn timwn

    # mo.sort(key=lambda x: x[1], reverse=True)
    # print("Process: Finding optimal order of preference OK!")
    # print("len_mo_array:", len(mo))
    # print("mo", mo)
    # print("len_results:", len(results["hits"]["hits"]))

    # print("Process: Preparing result file...")

    # new_results = results
    # row = 0
    # for movie in range(len(mo)):  #kratame mono tainies apotelesmatwn
    #     for movie_result in range(len(results["hits"]["hits"])):  # gia to plh8os twn apotelesmatvn ths es (new result)    ???? (eeinai mono ta hit|hit?)
    #         # print("movie_id     ", results["hits"]["hits"][movie_result]["_source"]["movieId"])
    #         # print("mo[movie][0]:", mo[movie][0])
    #         if int(mo[movie][0]) == int(results["hits"]["hits"][movie_result]["_source"]["movieId"]):
    #             score_array.append([mo[movie][0], mo[movie][1]])
    #             new_results["hits"]["hits"][row]["_index"] = results["hits"]["hits"][movie_result]["_index"]
    #             new_results["hits"]["hits"][row]["_type"] = results["hits"]["hits"][movie_result]["_type"]
    #             new_results["hits"]["hits"][row]["_id"] = results["hits"]["hits"][movie_result]["_id"]
    #             new_results["hits"]["hits"][row]["_score"] = mo[movie][1]
    #             new_results["hits"]["hits"][row]["_source"]["movieId"] = results["hits"]["hits"][movie_result]["_source"]["movieId"]
    #             new_results["hits"]["hits"][row]["_source"]["title"] = results["hits"]["hits"][movie_result]["_source"]["title"]
    #             new_results["hits"]["hits"][row]["_source"]["genres"] = results["hits"]["hits"][movie_result]["_source"]["genres"]
    #             row = row + 1
    #             continue

    # print("Process: Preparing result file OK!")
    # print("results    ", results)
    # print("new results", new_results)
    # print("score_array:", score_array)

    # print("write your query:")
    # query = input()
    # print("write your id:")
    # user_id_input = int(input())

while True:
    query = input('Write your query:')
    if(query == 'q'):
        break
    user_id = int(input('Write your id:'))

    es_results = es.search(index="movies", body={"size":100,"query": {"match": {'title': query}}})

    df_es = pd.DataFrame(pd.DataFrame(es_results['hits']['hits'])[['_score','_source']])
    df_es_source = pd.DataFrame(list(df_es['_source']))
    df_es = df_es.merge(df_es_source,left_index=True,right_index=True)
    df_es = df_es.drop('_source',axis=1)
    df_es = df_es.rename(columns={'_score':'score'})
    print(df_es)
