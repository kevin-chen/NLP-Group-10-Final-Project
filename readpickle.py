import pickle

# lexile_levels.pickle full_texts.pickle labeled_data.pickle

with open('labeled_data.pickle', 'rb') as f:
    data = pickle.load(f)
    print(data)