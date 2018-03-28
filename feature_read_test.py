import pickle

with open ('feature1', 'rb') as fp:
    itemlist = pickle.load(fp)

print(len(itemlist))