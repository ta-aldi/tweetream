from joblib import load
import os

class Classifier():

    # load model
    def __init__(self, model_path):
        self.model = load(model_path)

    # classify
    def run(self, text):
        return self.model.predict([text])[0]


clf_path = os.path.abspath('utils/LinSVCModel.joblib')
clf = Classifier(clf_path)
print(clf.run('jakarta lagi macet'))
print(clf.run('jakarta ibu kota negara indonesia'))
