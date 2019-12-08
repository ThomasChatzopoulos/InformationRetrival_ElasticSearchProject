array = [[1,2],[3,4,5],[5,6],[7,8]]
mo = []

for index in array:
    sum = 0 
    for value in index:
        sum += value
    mo.append(sum/len(index))

print(mo)

