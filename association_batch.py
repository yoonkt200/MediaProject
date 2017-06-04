from apyori import apriori

dataset = [["1","3","4"], ["2","3","5"], ["1","2","3","5"], ["2","5"]]
results = list(apriori(dataset))
results.sort(key=lambda x: x.support, reverse=True)
results = [item for item in results if item.support >= 0.5 and len(item.items) > 1]

results_array = []
for result in results:
    if "2" in result.items:
        print("item : ", result.items, "\tsupport : ", result.support * 100, "%")
        appended_items = ""
        for iteM in list(result.items):
            appended_items = appended_items + ", " + iteM
        appended_items = appended_items[2:]
        results_array.append([appended_items, result.support*100])

print (results_array[:2])


# results = [item for item in results if item.support >= 0.5 and len(item.items) > 1]