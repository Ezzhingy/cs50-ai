import nltk
import sys
import os
import string
import math


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():


    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }

    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    all_files = {}
    filenames = os.listdir(directory)
    for filename in filenames:
        with open(os.path.join(directory, filename), "r") as file_in:
            s = file_in.read()
            all_files[filename] = s
    return all_files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """    
    document = document.lower()
    document = document.translate(str.maketrans('','',string.punctuation))

    tokens = nltk.word_tokenize(document)
    tokens = [x for x in tokens if x not in nltk.corpus.stopwords.words("english")]

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_dct = {}
    for word_lst in documents.values():
        for word in word_lst:
            count = 0
            for temp_word_lst in documents.values():

                # if a word is in a file, increase count 
                if word in temp_word_lst:
                    count += 1
            
            idf = math.log(len(documents)/count)
            idf_dct[word] = idf
    return idf_dct
        

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    all_files_score = {}
    best_files = []

    for filename, lst_words in files.items():
        total = 0

        for query_word in query:

            #if query word is in a file containing the word
            if query_word in lst_words:

                # term frequency, num times word appears in the file
                tf = lst_words.count(query_word)

                # tf value multiplied by idf value of that same query word
                tf_idf = tf * idfs[query_word]

                # add this query tf_idf value to the total value for that file
                total += tf_idf
        
        # add the total pts for that file
        all_files_score[filename] = total

    # sorting dictionary in descending order
    sorted_dct = {}
    sorted_keys = sorted(all_files_score, key=all_files_score.get, reverse=True)
    for key in sorted_keys:
        sorted_dct[key] = all_files_score[key]
    
    count = 0 
    for best_filename in sorted_dct.keys():
        best_files.append(best_filename)
        count += 1
        if count == n:
            break
    
    return best_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_calc = {}
    query_term_density = {}
    sentence_name = []
    sentence_rank = []
    for query_word in query:
        for sent, sent_words in sentences.items():
            if query_word in sent_words:
                idf_value = idfs[query_word]

                if sent not in sentence_calc:
                    sentence_calc[sent] = 0
                    query_term_density[sent] = 0
                sentence_calc[sent] += idf_value
                query_term_density[sent] += sent_words.count(query_word)
    
    # sorting dictionary in descending order
    sorted_dct = {}
    sorted_keys = sorted(sentence_calc, key=sentence_calc.get, reverse=True)
    for key in sorted_keys:
        sorted_dct[key] = sentence_calc[key]
    

    # if n is just one, count needs to be -1 to account for first place tie
    count = -1
    for key, value in sorted_dct.items():
        sentence_rank.append((key, value))
        count += 1
        if count == n:
            break
    
    dup = False
    for i in range(n-1):
        
        # keep track of when values are swapped
        if dup == True:
            dup = False
            continue

        # if same value, check for higher query term density
        if sentence_rank[i][1] == sentence_rank[i+1][1]:
            if (query_term_density[sentence_rank[i][0]] / len(sentences[sentence_rank[i][0]])) > (query_term_density[sentence_rank[i+1][0]] / len(sentences[sentence_rank[i+1][0]])):
                sentence_name.append(sentence_rank[i][0]) 
            else: 
                sentence_name.append(sentence_rank[i+1][0])
                sentence_name.append(sentence_rank[i][0]) 
                dup = True
        else:
            sentence_name.append(sentence_rank[i][0])
    
    # if not enough sentences, add one more
    if len(sentence_name) != n:
        sentence_name.append(sentence_rank[n-1][0])
    
    # accommodates for when n = 1
    if n == 1:
        sentence_name.clear()
        if sentence_rank[0][1] == sentence_rank[1][1]:
            if (query_term_density[sentence_rank[0][0]] / len(sentences[sentence_rank[0][0]])) > (query_term_density[sentence_rank[1][0]] / len(sentences[sentence_rank[1][0]])):
                sentence_name.append(sentence_rank[0][0]) 
            else: 
                sentence_name.append(sentence_rank[1][0])
        else:
            sentence_name.append(sentence_rank[0][0])

    return sentence_name



if __name__ == "__main__":
    main()
