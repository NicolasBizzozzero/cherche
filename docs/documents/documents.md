# Documents

When using Cherche, you must define a document as a Python dictionary. A set of documents is simply a list of dictionaries. The name of the fields of the documents does not matter. You can choose the field(s) of your choice to perform neural search. It is mandatory to have a unique identifier for each document. The name of this identifier is up to you. In the example below, the identifier is the `id` field.

It can happen that not all documents have the same fields. You don't need to standardize or fill all the fields except for the identifier, i.e `id` in the example below.

```python
[
    {
        "id": 0,
        "title": "Paris",
        "url": "https://en.wikipedia.org/wiki/Paris",
        "article": "Paris (French pronunciation: \u200b[paʁi] (listen)) is the capital and most populous city of France, with an estimated population of 2,175,601 residents as of 2018, in an area of more than 105 square kilometres (41 square miles).",
    },
    {
        "id": 1,
        "title": "Paris",
        "url": "https://en.wikipedia.org/wiki/Paris",
        "article": "Since the 17th century, Paris has been one of Europe's major centres of finance, diplomacy, commerce, fashion, gastronomy, science, and arts.",
    },
    {
        "id": 2,
        "title": "Paris",
        "url": "https://en.wikipedia.org/wiki/Paris",
        "article": "The City of Paris is the centre and seat of government of the region and province of Île-de-France, or Paris Region, which has an estimated population of 12,174,880, or about 18 percent of the population of France as of 2017.",
    },
]
```
