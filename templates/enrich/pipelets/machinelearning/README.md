# Squirro Machine Learning Pipelet

This pipelet allows you to modify new items coming in using a Machine Learning workflow which has been successfully trained at least one.

## Usage
The pipelet takes a JSON configuration object of the form:
```json
{
    "cluster": "https://my-cluster.com",
    "token": "SQUIRRO_REFRESH_TOKEN",
    "project_id": "PROJECT_ID",
    "ml_workflow_id": "ML_WORKFLOW_ID"
}
```
