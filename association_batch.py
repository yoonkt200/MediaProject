from apyori import apriori

dataset = [["1","3","4"], ["2","3","5"], ["1","2","3","5"], ["2","5"]]
results = list(apriori(dataset))
results.sort(key=lambda x: x.support, reverse=True)
results = [item for item in results if item.support >= 0.5 and len(item.items) > 1]
results = results[:5]

results_array = []
for result in results:
    print("item : ", result.items, "\tsupport : ", result.support*100, "%")
    results_array.append([list(result.items), result.support*100])

print (results_array)