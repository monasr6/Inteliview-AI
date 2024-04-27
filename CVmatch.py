import fitz
import re
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec

def cleanText(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', ' ', text) # Remove email
    text = re.sub(r'[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', ' ', text) # Remove links google.com
    text = re.sub('https?\\S+', ' ', text)  # Remove URLs https://google.com
    text = re.sub('@S+', '  ', text)  # Remove mentions
    # Convert the text to lowercase
    text = text.lower()
    # Remove punctuation from the text except # for its special uses (C#)
    text = re.sub('[^a-z|#]', ' ', text)
    # Remove numerical values from the text
    text = re.sub(r'\d+', ' ', text)
    # Remove extra whitespaces
    text = re.sub(r"\s+", ' ', text)
    # Remove one character word
    text = re.sub(r'\s\w\s',r' ', text)
    # Remove stopwords
    text = " ".join(stopwords_removal(text.split(" ")))
    return text

def stopwords_removal(token_list):
    stop_words = (stopwords.words('english'))
    stop_words.append('faculty')
    stop_words.append('phonenumber')
    stop_words.append('university')

    stopwords_filtered_list = [w for w in token_list if w not in stop_words]
    return stopwords_filtered_list


def read_resume(filePath):
    with fitz.open(filePath) as doc:
        resume = ""
        for page in doc:
            resume += page.get_text()
        return resume
# def read_resume(pdfData):
#     resume = ""
#     with fitz.open("pdf", pdfData) as doc:
#         for page in doc:
#             resume += page.get_text()
#     print("cv : ",resume)
#     return resume

def apply_clean_context(jd,filePath):
    resume = read_resume(filePath)
    input_CV = cleanText(resume).split(" ")
    input_JD = cleanText(jd).split(" ")
    # removing duplicates
    # input_CV = set(input_CV)
    input_CV = [element for index, element in enumerate(input_CV) if element not in input_CV[:index]]
    # input_JD = set(input_JD)
    input_JD = [element for index, element in enumerate(input_JD) if element not in input_JD[:index]]
    return input_CV,input_JD

def CVmatching(jd,filePath):
    # Model evaluation
    model = Doc2Vec.load('/home/Inteliview/mysite/cv_job_maching.model')
    input_CV,input_JD = apply_clean_context(jd,filePath)
    model.random.seed(0)
    # v1 = model.infer_vector(input_CV)
    # model.random.seed(0)
    # v2 = model.infer_vector(input_JD)
    # similarity = (np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1)) * norm(np.array(v2)))*100
    similarity = model.similarity_unseen_docs(input_CV, input_JD, alpha=1, min_alpha=0.0001)
    similarity = similarity*100
    return round(similarity, 2)


