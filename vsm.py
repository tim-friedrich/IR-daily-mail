from collections import defaultdict
import pickle
import math
from helper.csv_helper import CsvHelper


def defaultdict_init():
    return defaultdict(int)


class VSM:
    def __init__(self, index, rebuild_index=False):
        self.index = index

        # length: a defaultdict whose keys are document ids, with values equal
        # to the Euclidean length of the corresponding document vector.
        self.length = defaultdict(float)

        self.dictionary = self.index.index.keys()
        self.N = CsvHelper.get_file_length(self.index.index.get_file()) - 1

        # As a result, postings[term] is the postings list for term, and
        # postings[term][id] is the frequency with which term appears in
        # document id.
        # postings
        if rebuild_index:
            self.frequency = defaultdict(defaultdict_init)
        else:
            with open('out/frequency', 'rb') as file:
                self.frequency = pickle.load(file)

    def __del__(self):
        if self.frequency:
            with open('out/frequency', 'wb') as output:
                pickle.dump(self.frequency, output, pickle.HIGHEST_PROTOCOL)

    def add_term(self, commend_id, term):
        self.frequency[term][commend_id] += 1

    def imp(self, term, id):
        """Returns the importance of term in document id.  If the term
        isn't in the document, then return 0."""
        if id in self.frequency[term]:
            return self.frequency[term][id] * self.inverse_document_frequency(term)
        else:
            return 0.0

    def inverse_document_frequency(self, term):
        """Returns the inverse document frequency of term.  Note that if
        term isn't in the dictionary then it returns 0, by convention."""

        if term in self.dictionary:
            return math.log(self.N / len(self.index.get_postings(term)), 2)
        return 0.0

    def similarity(self, query, id):
        """Returns the cosine similarity between query and document id.
        Note that we don't bother dividing by the length of the query
        vector, since this doesn't make any difference to the ordering of
        search results."""
        similarity = 0.0
        for term in query.split(' '):
            if term in self.dictionary:
                similarity += self.inverse_document_frequency(term) * self.imp(term, id)

        if self.length[id] > 0:
            similarity = similarity / self.length[id]
        return similarity
