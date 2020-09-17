# XXX Pipelet

This pipelet allows you to ...
When re-running the pipelet, you can use the `--query` parameter to limit the items that are processed.

## Usage
The pipelet takes a JSON configuration object of the form:
```json
{
    "key": "value",
}
```

## Version Tracking
You can use a version keyword to track which items have been processed by the pipelet. By deafult, a value of '1' is added to the facet `pipelet_version`.
You can change the version number and/or version facet name using the pipelet config by specifying:
```json
{
    "version": "3",
    "version_facet": "enrichment_version"
}
```
You can also disable version tracking completely by specifying
```json
{
    "version": false
}
```
