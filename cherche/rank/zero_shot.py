__all__ = ["ZeroShot"]

import typing

from ..compose import Intersection, Pipeline, Union


class ZeroShot:
    """ZeroShot classifier for ranking.

    Parameters
    ----------
    on
        Fields to use to match the query to the documents.
    encoder
        Zero shot classifier to use for ranking
    k
        Number of documents to retrieve. Default is None, i.e all documents that match the query
        will be retrieved.
    multi_class
        If more than one candidate label can be correct, pass multi_class=True to calculate each
        class independently.

    Examples
    --------

    >>> from pprint import pprint as print
    >>> from cherche import rank
    >>> from transformers import pipeline
    >>> from sentence_transformers import SentenceTransformer

    >>> documents = [
    ...    {"title": "Paris", "article": "This town is the capital of France", "author": "Wiki"},
    ...    {"title": "Eiffel tower", "article": "Eiffel tower is based in Paris", "author": "Wiki"},
    ...    {"title": "Montreal", "article": "Montreal is in Canada.", "author": "Wiki"},
    ... ]

    >>> ranker = rank.ZeroShot(
    ...     encoder = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli"),
    ...     on = ["title", "article"],
    ...     k = 2,
    ... )

    >>> ranker
    Zero Shot Classifier
         model: typeform/distilbert-base-uncased-mnli
         on: title, article
         k: 2
         multi class: True

    >>> print(ranker(q="Paris", documents=documents))
    [{'article': 'This town is the capital of France',
      'author': 'Wiki',
      'similarity': 0.44725707173347473,
      'title': 'Paris'},
     {'article': 'Eiffel tower is based in Paris',
      'author': 'Wiki',
      'similarity': 0.31512799859046936,
      'title': 'Eiffel tower'}]

    References
    ----------
    1. [New pipeline for zero-shot text classification](https://discuss.huggingface.co/t/new-pipeline-for-zero-shot-text-classification/681)
    2. [NLI models](https://huggingface.co/models?pipeline_tag=zero-shot-classification&sort=downloads)

    """

    def __init__(
        self, encoder, on: typing.Union[str, list], k: int = None, multi_class: bool = True
    ):
        self.encoder = encoder
        self.on = on if isinstance(on, list) else [on]
        self.k = k
        self.multi_class = multi_class

    def __repr__(self) -> str:
        repr = "Zero Shot Classifier"
        repr += f"\n\t model: {self.encoder.tokenizer.name_or_path}"
        repr += f"\n\t on: {', '.join(self.on)}"
        repr += f"\n\t k: {self.k}"
        repr += f"\n\t multi class: {self.multi_class}"
        return repr

    def __call__(self, q: str, documents: list, **kwargs) -> list:
        """Rank inputs documents based on query.

        Parameters
        ----------
        q
            Inputs query.
        documents
            List of documents to rank.

        """
        if not documents:
            return []

        scores = self.encoder(
            q,
            [" ".join([document[field] for field in self.on]) for document in documents],
            multi_label=self.multi_class,
        )

        ranked = []
        for label, score in zip(scores["labels"], scores["scores"]):
            for document in documents:
                content = " ".join([document[field] for field in self.on])
                if content == label:
                    ranked.append(document)
                    document.update({"similarity": score})
        return ranked[: self.k] if self.k is not None else ranked

    def __add__(self, other) -> Pipeline:
        """Custom operator to make pipeline."""
        if isinstance(other, Pipeline):
            return other + self
        else:
            return Pipeline(models=[other, self])

    def __or__(self, other) -> Union:
        """Custom operator for union."""
        if isinstance(other, Union):
            return Union(models=[self] + [other.models])
        else:
            return Union(models=[self, other])

    def __and__(self, other) -> Intersection:
        """Custom operator for intersection."""
        if isinstance(other, Intersection):
            return Intersection(models=[self] + [other.models])
        else:
            return Intersection(models=[self, other])

    def add(self, documents) -> "ZeroShot":
        """Zero shot do not pre-compute embeddings."""
        return self
