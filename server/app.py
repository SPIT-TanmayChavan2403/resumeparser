from flask import Flask,  jsonify
from flask_cors import CORS
from flask import request
import scorer, json, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer, util
import nltk

app = Flask(__name__)
CORS(app)

# The directory where the files will be saved
UPLOAD_FOLDER = "Resume"

@app.route("/upload", methods=["POST"])
def upload_files():
    # Loop through the files in request.files
    for file in request.files.values():
        # Get the file name and extension
        filename = file.filename
        # Save the file to the upload folder
        file.save(UPLOAD_FOLDER + "/" + filename)
    # jd = json.loads(request.data.decode("utf-8"))
    resp = run(request.form['algo'] , request.form['job_description'])
    print("this is the algo", request.form['algo'])

    for file in request.files.values():
        os.remove(UPLOAD_FOLDER + "/" + file.filename)  
    sorted_resp = dict(sorted(resp.items(), key=lambda item: item[1], reverse=True))
    response = []

    for key, value in sorted_resp.items():
        response.append(f"Score of {key} is : {value}")
    return jsonify(response)

def preprocess(document):
    stop_words = []
    try:
        with open('./stopWords.txt', 'r') as f:
            stop_words = f.read().split(',')
    except Exception as e:
        print('Error while reading stopwords.txt', e)

    words = document.split()
    filtered_words = [word for word in words if word not in stop_words]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    lowercased_words = [word.lower() for word in stemmed_words]
    preprocessed_document = ' '.join(lowercased_words)
    return preprocessed_document

def bert(pdf_path, target_document):
    provided_documents = extract_text(pdf_path)

    target_document = preprocess(target_document)
    provided_documents = [preprocess(provided_documents)]

    # Load a pre-trained BERT model (e.g., from Hugging Face Transformers or Sentence Transformers)
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Encode the target document and provided documents into dense embeddings
    target_embedding = model.encode(target_document, convert_to_tensor=True)
    provided_embeddings = model.encode(provided_documents, convert_to_tensor=True)

    # Calculate cosine similarity between the target document and provided documents
    cosine_scores = util.pytorch_cos_sim(target_embedding, provided_embeddings)

    # Print similarity scores for each provided document
    for i, score in enumerate(cosine_scores):
        return score[0]*100

def tfidf(pdf_path, target_document):
    provided_documents = extract_text(pdf_path)

    target_document = preprocess(target_document)
    provided_documents = [preprocess(provided_documents)]

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Combine the target document and provided documents into a list
    all_documents = [target_document] + provided_documents

    # Fit the vectorizer on the documents and transform them into TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)

    # Calculate the cosine similarity between the target document and provided documents
    cosine_similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Print similarity scores
    for i, score in enumerate(cosine_similarity_scores):
        return (score*100)

def run(algo, jd):
    path = os.getcwd() + "/Resume"
    files = os.listdir(path)
    resp = {}
    for file in files:
        if (algo == 'BERT'):
            resp[file] = bert(path + "/" + file, jd)
        else:
            resp[file] = tfidf(path + "/" + file, jd)
    return resp

if __name__ == '__main__':
    app.run(debug=True)