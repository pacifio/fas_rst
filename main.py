#!/usr/bin/env python3

"""
FAS RST Gen 1

Falcon Academy of Sciences Reasearch paper Summarization Tool

This is a generic text summarization tool modified to summarize PDF content , still not stable
This needs to implement deep Learning algorithms , currently implemented only using spacY library
SpacY uses text extraction algorithms which looks for certain tokens

Please see README.md for more instructions
"""

import os
import sys
import spacy
from heapq import nlargest
from string import punctuation as punc
from spacy.lang.en.stop_words import STOP_WORDS
from PyPDF2 import PdfReader
from tika import parser


# If production mode is `False` then `test()` function will be called
PRODUCTION_MODE = True

# Use Apache Tika to extract PDF content , this is recommended but needs JAVA RE to work
USE_TIKA_SERVER = True

demos = {
    'demo1': """The human coronavirus was first diagnosed in 1965 by Tyrrell and Bynoe from the respiratory tract sample of an adult with a common cold cultured on human embryonic trachea.1 Naming the virus is based on its crown-like appearance on its surface.2 Coronaviruses (CoVs) are a large family of viruses belonging to the Nidovirales order, which includes Coronaviridae, Arteriviridae, and Roniviridae families.3 Coronavirus contains an RNA genome and belongs to the Coronaviridae family.4 This virus is further subdivided into four groups, ie, the α, β, γ, and δ coronaviruses.5 α- and β-coronavirus can infect mammals, while γ- and δ- coronavirus tend to infect birds.6 Coronavirus in humans causes a range of disorders, from mild respiratory tract infections, such as the common cold to lethal infections, such as the severe acute respiratory syndrome (SARS), Middle East respiratory syndrome (MERS) and Coronavirus disease 2019 (COVID-19). The coronavirus first appeared in the form of severe acute respiratory syndrome coronavirus (SARS-CoV) in Guangdong province, China, in 20027 followed by Middle East respiratory syndrome coronavirus (MERS-CoV) isolated from the sputum of a 60-year-old man who presented symptoms of acute pneumonia and subsequent renal failure in Saudi Arabia in 2012.8 In December 2019, a β-coronavirus was discovered in Wuhan, China. The World Health Organization (WHO) has named the new disease as Coronavirus disease 2019 (COVID-19), and Coronavirus Study Group (CSG) of the International Committee has named it as SARS-CoV-2.9,10 Based on the results of sequencing and evolutionary analysis of the viral genome, bats appear to be responsible for transmitting the virus to humans""",
    'demo2': """Abstract. We address the question of which convex shapes, when
packed as densely as possible under certain restrictions, fill the least
space and leave the most empty space. In each different dimension and under each different set of restrictions, this question is
expected to have a different answer or perhaps no answer at all.
As the problem of identifying global minima in most cases appears
to be beyond current reach, in this paper we focus on local minima. We review some known results and prove these new results:
in two dimensions, the regular heptagon is a local minimum of
the double-lattice packing density, and in three dimensions, the
directional derivative (in the sense of Minkowski addition) of the
double-lattice packing density at the point in the space of shapes
corresponding to the ball is in every direction positive.""",
    'demo3':  """An n-dimensional convex body is a convex, compact, subset of R
n
with nonempty interior. The space of convex bodies, denoted Kn
, can
be endowed with the Hausdorff metric:
dist(K, K0
) = min{ε : K0 ⊆ Kε and K ⊆ K0
ε},
where Kε = {x + y : x ∈ K, ||y|| ≤ ε} is the ε-parallel body of K.
A set of isometries Ξ is said to be admissible for K if the interiors
of ξ(K) and ξ
0
(K) are disjoint for all distinct ξ, ξ0 ∈ Ξ. The (lower)
mean volume of Ξ can be defined as d(Ξ) = lim infr→∞(4πr3/3)/|{ξ ∈
Ξ : ||ξ(0)|| < r}|. The collection {ξ(K) : ξ ∈ Ξ} for an admissible Ξ is
called a packing of K and said to be produced by Ξ. Its density is the
fraction of space it fills: vol(K)/d(Ξ). The packing density of a body
K, denoted δ(K) is the supremum of vol(K)/d(Ξ) over all admissible
sets of isometries. Groemer proves some basic results about packing
densities, including the fact that the supremum is actually achieved
by some packing and the fact that δ(K) is continuous [10]. Groemer’s
result apply also to the restricted packing densities which we define
below."""
}


# Private _Summarizer utility class
class _Summarizer():
    @staticmethod
    def summarize(text: str) -> str:
        stopwords = list(STOP_WORDS)
        punctuation = punc + '\n'

        nlp = spacy.load('en_core_web_sm')  # Core english language model
        doc = nlp(text)

        word_frequencies = {}  # Reduce word by frequencies
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1

        max_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_frequency

        sentence_tokens = [sent for sent in doc.sents]

        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

        select_length = int(len(sentence_tokens)*0.3)
        select_length
        summary = nlargest(select_length, sentence_scores,
                           key=sentence_scores.get)

        final_summary = [word.text for word in summary]
        summary = ''.join(final_summary)

        return summary

    @staticmethod
    def log(original: str = "", summary: str = "") -> None:
        print("================= ORIGINAL =================")
        print(f"LEN : {len(original)}\n")
        print("================= SUMMARY =================")
        print(f"LEN : {len(summary)}\n")

    @staticmethod
    def save_txt(text: str) -> None:
        if (len(text) > 0):
            with open("summary.txt", "w") as f:
                f.write(text)


class PdfUtils():
    @staticmethod
    def read(filename: str) -> str:
        reader = PdfReader(filename)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    @staticmethod
    def read_with_tika(filename: str) -> str:
        raw = parser.from_file(filename)
        return raw['content']


def test() -> None:
    text = demos['demo3']
    r = _Summarizer.summarize(text)
    _Summarizer.log(text, r)
    _Summarizer.save_txt(r)


def compute(filename: str) -> None:
    content = ""

    if USE_TIKA_SERVER:
        content = PdfUtils.read_with_tika(filename=filename).strip()
    else:
        content = PdfUtils.read(filename=filename).strip()

    with open("original.txt", "w") as f:
        f.write(content)
        print("Original content written to original.txt")

    summary = _Summarizer.summarize(text=content)
    _Summarizer.save_txt(text=summary)
    print("Summary saved to summary.txt")


def main() -> None:
    filename = sys.argv[1]
    if filename is None or (len(str(filename)) < 0):
        print("File path not found")
        sys.exit(0)
    else:
        if os.path.exists(filename):
            if filename.endswith(".pdf"):
                compute(filename=filename)
            else:
                print("File must be a pdf file . E.G sample.pdf")
                sys.exit(0)
        else:
            print("File does not exist , Quitting")
            sys.exit(0)


if __name__ == "__main__":
    if PRODUCTION_MODE:
        main()
    else:
        test()
