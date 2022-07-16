import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    """
    ACTUAL VALUES ADD TO 1, BUT ROUNDED VALUES ADD TO 1.0001
    """
    # total = 0
    # for value in ranks.values():
    #     total += value
    # print(total)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    
    """
    ACTUAL VALUES ADD TO 1, BUT ROUNDED VALUES ADD TO 1.0001
    """
    # total = 0
    # for value in ranks.values():
    #     total += value
    # print(total)

    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution = {}

    if page == set():
        for key in corpus:
            prob_distribution[key] = 1 / len(corpus)
    else:
        for key in corpus:
            
            if page == key:
                connected = corpus[key]

                for p in connected:
                    prob_distribution[p] = damping_factor / len(connected)

            if key in prob_distribution:
                prob_distribution[key] += (1 - damping_factor) / len(corpus)
            else:
                prob_distribution[key] = (1 - damping_factor) / len(corpus)

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    total_sample = []
    current_sample = random.choice(list(corpus))
    total_sample.append(current_sample)

    for i in range(n):
        prob_distribution = transition_model(corpus, current_sample, damping_factor)
        
        prob = []
        page = []
        for item in prob_distribution.items():
            page.append(item[0])
            prob.append(item[1])
        
        current_sample = "".join(map(str, random.choices(page, prob)))
        total_sample.append(current_sample)
        
    count = 0
    for i in total_sample:
        if i not in pagerank:
            pagerank[i] = 0
        pagerank[i] += 1
        count += 1
    
    for item in pagerank.items():
        pagerank[item[0]] = item[1] / count
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    temp = {}

    N = len(corpus)
    page = []

    for key in corpus:
        pagerank[key] = 1 / N
        temp[key] = 1 / N
        page.append(key)

    for key in corpus:
        if corpus[key] == set():
            page.remove(key)
            corpus[key] = page

    diff = math.inf
    while diff > 0.001:
        for key in pagerank:

            pages_linking = []

            for item in corpus.items():
                if key in item[1]:
                    pages_linking.append(item[0])
            
            second_condition = 0

            for page in pages_linking:
                PR_i = pagerank[page]
                Numlinks_i = len(corpus[page])

                second_condition += PR_i / Numlinks_i
            formula = ((1 - damping_factor) / N) + (damping_factor * second_condition)

            temp[key] = formula
        
        for key in temp:
            diff = abs(temp[key] - pagerank[key])
            if diff > 0.001:
                break
        
        pagerank = temp.copy()
    
    return pagerank


if __name__ == "__main__":
    main()
