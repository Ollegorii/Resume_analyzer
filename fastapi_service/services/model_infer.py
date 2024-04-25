import logging

import joblib
from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer
from pymystem3 import Mystem
from string import punctuation
import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from fastapi_service.services.model_preprocc import inference
import numpy as np
from pydantic import BaseModel

bow = joblib.load("fastapi_service/static2/models_weights/bow.pkl")
tfidf = joblib.load("fastapi_service/static2/models_weights/tfidf.pkl")
w2v_wv = KeyedVectors.load("fastapi_service/static2/models_weights/word2vec.wordvectors", mmap='r')
sbert = SentenceTransformer("fastapi_service/static2/models_weights/sbert_weights")
means = pd.read_pickle("fastapi_service/static2/models_weights/means.pkl")
resume_mean_sbert = means['mean_resume'].values
vac_mean_sbert = means['mean_vac'].values
X = np.load('fastapi_service/static2/data/embed.npy')
resume_url = pd.read_csv('fastapi_service/static2/resume_url_data.csv')
resumes_texts = pd.read_csv('fastapi_service/static2/resume_url_texts.csv')
mystem = Mystem(disambiguation=False)

punctuation = list(punctuation)


k = 5
nbrs_sbert = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='cosine').fit(X)


def model_infer(vac_text, res_text):
    resume_vac_texts = pd.DataFrame({"resume": [vac_text], "vaccancy": [res_text]})
    return inference(resume_vac_texts, sbert, bow, tfidf, w2v_wv, mystem, stopwords.words("russian"),
                     punctuation, resume_mean_sbert, vac_mean_sbert, "max", 0.2)


class Resume(BaseModel):
    job: str = ""
    url: str = ""
    number: str = ""

def knn_infer(vacancy_text, resume_url, resumes_texts, sbert, vac_mean_sbert):
    vacancy = sbert.encode([vacancy_text])
    distances, indices = nbrs_sbert.kneighbors(vacancy - vac_mean_sbert)
    data = []
    for j, i in enumerate(indices[0]):
        data.append(Resume(
            job=resume_url.job.iloc[i],
            url=resume_url.url.iloc[i],
            number=str(distances[0][j]),
        ))

    return data
def model_knn_infer(vacancy):

    return knn_infer(vacancy, resume_url, resumes_texts, sbert, vac_mean_sbert)

