# Pipelet Templates

So you want to write a pipelet...

## Templates
There are three different base templates included here:
* `minimal`: The absolute minimum
* `caching`: A template that includes the HTTP Response caching framework. Useful for building pipelets that leverage external web services.
* `version_tracking`: A template that includes a version tracking facet. Not always necessary but very useful if you want to be able to track which items have already been processed by the pipelet, or to be able to do multiple iterations of the enrichment.
* `file_data`: A template that provides an easy way to access raw data for files like PDF documents

### Choosing a Template
To simplify things, you should pick a template depending on what the pipelet will be doing
* Simple transformation of data as it is loaded into squirro, using no external resources
  * Use the minimal template
* Re-processing data that is already loaded into Squirro
  * Use the version_tracking template
* Enriching data using a 3rd party API
  * Use the caching tempalte
* Buildign a pipelet that has to access the raw data for a file like a PDF (and will run server-side)
  * Use the file_data template

## Supporting Files
Templates for supporting files are also provided. These are:
* `pipelets.json`: Template for a pipelets config file used by the Squirro Data Loader to specify enrichments to be run before data is loaded into squirro
* `rerun_pipelet.sh`: Template for a shell script used to rerun a pipelet against the data already in a Squirro project using the pipelet cli tool.
* `upload_pipelet.sh`: Template for a shell scipt that uploads a pipelet to be used server-side using the pipelet cli tool.
