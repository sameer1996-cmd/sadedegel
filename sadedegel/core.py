from transformers import AutoTokenizer
from .tokenize import RegexpSentenceTokenizer
from .summarize import FirstK


class NLPPipeline:
    def __init__(self, sent_tokenizer=RegexpSentenceTokenizer(),
                 tokenizer=AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased"),
                 summarizer=FirstK(0.5)):
        self.sent_tok = sent_tokenizer
        self.summarizer = summarizer

        if isinstance(summarizer, FirstK):
            self.tokenizer = None
        else:
            self.tokenizer = tokenizer

    def __call__(self, doc):
        sents = self.sent_tok(doc)

        if self.tokenizer is None:
            summary = self.summarizer(sents)
        else:
            raise NotImplementedError("Summarization with a word tokenizer is not there yet.")

        return summary


class Summarizer:
    def __init__(self):
        self.pipeline = NLPPipeline()

    def __call__(self, doc):
        return self.pipeline(doc)


def load():
    """Extraction-based document summarizer pipeline

     Examples
     --------

     >>> from sadedegel import load
     >>> from sadedegel.dataset import load_raw_corpus
     >>> summarizer = load()
     >>> raw = load_raw_corpus(False)

     >>> news_summary = summarizer(raw[2])

     >>> len(raw[2])
     3179

     Default text summarizer only takes first half of the all sentences in document.
     >>> sum((len(sent) for sent in news_summary))
     1699

     """
    return Summarizer()