import nltk
import sys
import string

import ssl


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP Conj NP | NP Conj VP | NP PP Det N
AdjP -> Adj | Adj AdjP
PP -> P | P NP
NP -> N | Det N | AdjP NP | N PP | N VP | N Adv | N NP | Det AdjP N | Det N Adv
VP -> V | V NP | V NP PP | V PP Det N | V PP NP | Adv VP | V Adv
"""

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    token_sent = nltk.word_tokenize(sentence.lower())
    not_words = []

    for i in range(len(token_sent)):
        for char in token_sent[i]:
            if char not in string.ascii_lowercase:
                not_words.append(token_sent[i])
                break
    
    for not_word in not_words:
        token_sent.remove(not_word)
    
    return token_sent

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunk_lst = []
    for s in tree.subtrees():
        if s.label() == 'NP' and s not in np_chunk_lst:

            chunk = chunk_finder(s)                
            np_chunk_lst.append(chunk)
        
    return np_chunk_lst

def chunk_finder(subtree):
    s = subtree.subtrees()
    if peek(s) == -1:
        return subtree
    
    for ss in s:
        if ss.label() == 'NP':
            chunk = chunk_finder(ss)
            return chunk
    return subtree

def peek(subtree):
    try:
        first = next(subtree)
    except StopIteration:
        return -1
    return 0


if __name__ == "__main__":
    main()
