import json
import pickle

MODEL = "./model"
PARAMS = "./params"
for c in ["10^4", "10^5", "10^6", "all"]:
    with open(f"{MODEL}/nine_single_{c}.pkl", "rb") as f:
        rf = pickle.load(f)
    param = rf.get_params()
    print(type(param))
    print(param)
    with open(f"{PARAMS}/nine_single_{c}.json", "w") as f:
        json.dump(param, f, indent=4)
