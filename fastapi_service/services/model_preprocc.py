import pandas as pd
from sentence_transformers import util

import nltk
import re
from numpy import dot
from numpy.linalg import norm

nltk.download("stopwords")


def preprocess_text(text, stemmer, stopwords, punctuation):
    text = re.sub(r'\xa0', ' ', text)
    tokens = stemmer.lemmatize(text.lower())
    stopen_symbols = stopwords + punctuation + [' ']
    tokens = [token for token in tokens if token not in stopen_symbols]

    text = " ".join(tokens)

    return text


def get_mean_w2v_vector(sentence, wv):
    words = sentence.split()
    vectors = [wv[word] for word in words if word in wv]

    if vectors:
        return sum(vectors) / len(vectors)
    else:
        return 0


def w2v_emb_resume(text, w2v_wv, mean_resume=0):
    emb = get_mean_w2v_vector(text, w2v_wv) - mean_resume
    return emb


def vectorizer_emb_resume(text, vectorizer, mean_resume=0):
    emb = vectorizer.transform([text])
    emb = emb.toarray()[0] - mean_resume
    return emb


def sbert_emb_resume(sentence, sbert, mean_resume=0):
    embeddings = sbert.encode(sentence)
    emb = embeddings[0] - mean_resume
    return emb


def similarity(text1, text2, vectorizer, mean_resume=0, mean_vac=0):
    emb1 = vectorizer.transform([text1])
    emb2 = vectorizer.transform([text2])
    emb1 = emb1.toarray()[0] - mean_resume
    emb2 = emb2.toarray()[0] - mean_vac
    cos_sim = dot(emb1, emb2) / (norm(emb1) * norm(emb2))
    cos_sim = max(0, cos_sim)
    return cos_sim


def get_table_emb(resume_texts, sbert, w2v_wv, bow, tfidf, mystem, russian_stopwords, punctuation, resume_mean_sbert):
    resume_emb_data = pd.DataFrame(
        columns=['resume', 'w2v_embedding', 'bow_embedding', 'tfidf_embedding', 'sbert_embedding'])
    for index, row in resume_texts.iterrows():
        text = row['text']
        text = preprocess_text(text, mystem, russian_stopwords, punctuation)
        w2v_emb = w2v_emb_resume(text, w2v_wv)
        bow_emb = vectorizer_emb_resume(text, bow)
        tfidf_emb = vectorizer_emb_resume(text, tfidf)
        sbert_emb = sbert_emb_resume([row['text']], sbert, resume_mean_sbert)
        to_add = pd.DataFrame(
            {'resume': text, 'w2v_embedding': [w2v_emb], 'bow_embedding': [bow_emb],
             'tfidf_embedding': [tfidf_emb], 'sbert_embedding': [sbert_emb]})
        resume_emb_data = pd.concat([resume_emb_data, to_add], ignore_index=True)
    return resume_emb_data


def similarity_w2v(text1, text2, w2v_wv, agg_type='max', mean_resume=0, mean_vac=0):
    emb1 = get_mean_w2v_vector(text1, w2v_wv) - mean_resume
    emb2 = get_mean_w2v_vector(text2, w2v_wv) - mean_vac
    cos_sim = dot(emb1, emb2) / (norm(emb1) * norm(emb2))
    if agg_type == 'max':
        cos_sim = max(0, cos_sim)
    elif agg_type == 'displ':
        cos_sim = (1 + cos_sim) / 2
    return cos_sim


def similarity_sbert(sentences, sbert, mean_resume=0, mean_vac=0):
    embeddings = sbert.encode(sentences)
    cos_sim_sbert = (1 + util.cos_sim(embeddings[0] - mean_resume, embeddings[1] - mean_vac).item()) / 2
    return cos_sim_sbert


def aggregate_models(text1, text2, texts_for_bert, sbert, bow, tfidf, w2v_wv, mean_resume_sbert=0, mean_vac_sbert=0,
                     agg_type='max', threshold=0.2):
    cos_sim_w2v = similarity_w2v(text1, text2, w2v_wv, agg_type)
    cos_sim_bow = similarity(text1, text2, bow)
    cos_sim_tfidf = similarity(text1, text2, tfidf)
    cos_sim_sbert = similarity_sbert(texts_for_bert, sbert, mean_resume_sbert, mean_vac_sbert)
    sims = [cos_sim_w2v, cos_sim_bow, cos_sim_tfidf, cos_sim_sbert]
    #print(sims)
    if min(sims) < threshold:
        return min(sims)
    else:
        return max(sims)


def find_k_nearest(vac_text, k, resume_texts, sbert, bow, tfidf, w2v_wv, mystem, russian_stopwords, punctuation,
                   mean_resume_sbert, mean_vac_sbert, agg_type='max'):
    sims = []
    vac_text_proc = preprocess_text(vac_text, mystem, russian_stopwords, punctuation)
    for index, row in resume_texts.iterrows():
        resume_text = preprocess_text(row['text'], mystem, russian_stopwords, punctuation)
        sims.append([aggregate_models(resume_text, vac_text_proc, [vac_text, row['text']], sbert, bow, tfidf, w2v_wv,
                                      mean_resume_sbert, mean_vac_sbert, agg_type), row['text']])
    sims.sort(reverse=True)
    return sims[:k]


def inference_preprocc(resume_vac_texts: pd.DataFrame, sbert, bow, tfidf, w2v_wv, mystem, russian_stopwords,
                       punctuation, mean_resume_sbert, mean_vac_sbert, agg_type):
    result = []
    for index, row in resume_vac_texts.iterrows():
        resume = preprocess_text(row['resume'], mystem, russian_stopwords, punctuation)
        vacancy = preprocess_text(row['vaccancy'], mystem, russian_stopwords, punctuation)
        sim = aggregate_models(resume, vacancy, [row['resume'], row['vaccancy']], sbert, bow, tfidf, w2v_wv,
                               mean_resume_sbert, mean_vac_sbert, agg_type)
        result.append(sim)
    return result


def inference(resume_vac_texts: pd.DataFrame, sbert, bow, tfidf, w2v_wv, mystem, russian_stopwords, punctuation,
              mean_resume_sbert, mean_vac_sbert, agg_type, threshold):
    result = []
    for index, row in resume_vac_texts.iterrows():
        resume = preprocess_text(row['resume'], mystem, russian_stopwords, punctuation)
        vacancy = preprocess_text(row['vaccancy'], mystem, russian_stopwords, punctuation)
        sim = aggregate_models(resume, vacancy, [row['resume'], row['vaccancy']], sbert, bow, tfidf, w2v_wv,
                               mean_resume_sbert, mean_vac_sbert, agg_type, threshold)
        result.append(sim)
    return result
