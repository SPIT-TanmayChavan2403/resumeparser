import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from pdfminer.high_level import extract_text
import os

def start_process():
    # Sample target document (you should replace this with your target document)
    target_document = "We are looking for a qualified Front-end developer to join our IT team. You will be  responsible for building the ‘client-side’ of our web applications. You should be able to translate our company and customer needs into functional and appealing interactive applications. If you’re interested in creating a user-friendly environment by writing code and moving forward in your career, then this job is for you. We expect you to be a tech-savvy professional, who is curious about new digital technologies and aspires to combine usability with visual design. Ultimately, you should be able to create a functional and attractive digital environment for our company, ensuring great user experience. Responsibilities are as follow Use markup languages like HTML to create user-friendly web pages, Maintain and improve website, Optimize applications for maximum speed, Design mobile-based features, Collaborate with back-end developers and web designers to improve usability, Get feedback from, and build solutions for, users and customers, Write functional requirement documents and guides, Create quality mockups and prototypes, Help back-end developers with coding and troubleshooting, Ensure high quality graphic standards and brand consistency, Stay up-to-date on emerging technologies"

    # This array will store all the documents provided by the user.
    provided_documents = []

    def extract_text_from_pdf(pdf_path):
        provided_documents.append(extract_text(pdf_path))

    for i in range(1, 13):
        extract_text_from_pdf(f'{os.getcwd()}/Resume/file {i}.pdf');

    # Define the weighting parameter (α)
    alpha = 0.5  # You can optimize this parameter based on your experiments

    # It preprocesses the documents by removing the stop words and converting all the words to lower case
    def preprocess(document):
        words = document.split()
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in words]
        lowercased_words = [word.lower() for word in stemmed_words]
        preprocessed_document = ' '.join(lowercased_words)
        return preprocessed_document

    target_document = preprocess(target_document)
    provided_documents = [preprocess(doc) for doc in provided_documents]

    # Extract keywords from the target document
    target_keywords = set(target_document.split())

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    all_documents = [target_document] + provided_documents
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)

    # Calculate the cosine similarity between the target document and each provided document
    cosine_similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Calculate the association rule confidence for each provided document
    association_rule_confidences = []

    for provided_document in provided_documents:
        provided_keywords = set(provided_document.split())
        
        # Calculate the number of shared keywords
        shared_keywords_count = len(target_keywords.intersection(provided_keywords))
        
        # Calculate association rule confidence as the ratio of shared keywords to the total keywords in the provided document
        confidence = shared_keywords_count / len(provided_keywords)
        
        association_rule_confidences.append(confidence)

    # Calculate the similarity score for each provided document
    similarity_scores = []

    for i, similarity in enumerate(cosine_similarity_scores):
        similarity_score = alpha * similarity + (1 - alpha) * association_rule_confidences[i]
        similarity_scores.append(similarity_score)

    # Print the similarity scores for each provided document
    response = {}
    for i, score in enumerate(similarity_scores):
        key = f"Rank of Resume {i + 1}"
        print(f"{key}: {score*100}%")
        response[key] = score*100
    print("Final Response", response)
    return response

def main():
    return start_process()

if __name__ == "__main__":
    main()