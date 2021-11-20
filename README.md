# NLP & Elasticsearch powered product search

**Note:** this README assumes you already followed the instructions in the 1.5-es-improved branch README

## Introducing NLP

The underlying problem with previous versions of this app is that we don't actually understand what the user is asking
for. As humans, we understand that given the query 'a packable jacket' the user wants a jacket (product) with the
attribute/adjective of being packable. However, elasticsearch, like all full text search databases doesn't understand
this. It works at a field and term level - it doesn't understand human language. That's where NLP/NLU comes into it's
own.

This version of the code introduces very basic NLP capabilities, allowing us to distinguish between the desired product
and desired product attributes. It uses the Spacy framework to perform very primitive Named Entity Recognition (NER).
This is absolutely not an NLP or Spacy tutorial, the code and NLP model used is deliberately very basic. The purpose of
this code is simply to show how NLP can complement traditional full text search, making it much more powerful.

Subsequent versions of the app will extend the concept.

## Getting started

Kill the old server if it's still running

<kbd>Ctrl</kbd> + <kbd>c</kbd>

Bring up elasticsearch again if its no longer running:

```shell
$ docker-compose up -d elasticsearch-7
```

Install the new dependency:

```shell
$ pip install -r requirements.txt
...
Successfully installed spacy-3.1.4
```

Rerun the new server code

```shell
$ bin/server.sh
```

## Query again

```shell
$ python -m src.client 'packable jacket'
```

```json
{
    "ner_prediction": {
        "text": "packable jacket",
        "product": "jacket",
        "attrs": [
            "packable"
        ]
    },
    "results": [
        {
            "title": "lightweight black jacket",
            "product_type": "jacket",
            "price": 100.0,
            "attrs": [
                "lightweight",
                "black"
            ]
        }
    ]
}
```

## Changes to the code

The major change is the introduction of the NerPredictor in the new src/ner_predictor.py module. This class uses a
pretrained NLP model to perform Named Entity Recognition on the full text search query. It identifies the desired
product along with the desirable product attributes. This structured query is then passed into the elastic search query.

As the real "magic" happens in the NerPredictor, I've also added a new endpoint and client helper which simply performs
Named Entity Recognition on a query:

```shell
$ python -m src.client -p 'packable jacket'
```

```json
{
    "text": "packable jacket",
    "product": "jacket",
    "attrs": [
        "packable"
    ]
}
```