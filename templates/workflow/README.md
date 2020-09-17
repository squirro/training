# ML Workflows

Included here are templates for ML Workflows to facilitate common tasks.
The workflows are not meant to be used "as-is", but modified slightly to fit specific use cases. They are meant to serve as a good place to start to get you 90% of the way there

## Contents

* __topic_modeling__ - Use this if you have a fresh, raw text data set and want to be able to identify the significant topics and clusters of documents.
  * Example: I want to find the most common topics in recent news, even if it's something I've never seen before
  * Example: I want to find the most common issues out of a set of complaints from my clients
* __Classification__ - Use this if you have a specific topic or set of topics (that you already know) which you want to be able to classify text into.
  * Example: I want to load Email Messages and tag the ones that are about negotiation
  * Example: I want to find references to management changes in news articles
* __Recommendation__ - Use this if you want to recommend specific things like products or counterparties based on the "profile" of each.
  * Example: I want to recommend products to pitch a new client based on what similar clients have purchased in the past
  * Example: I want to find an investor in a new deal, based on who has invested in similar deals in the past
* __term_extraction__ - Use this if you want to extract key terms from each document, similar to a TFIDF embedder .
  * Please note this is not part of the product yet and requires a patch to use!
