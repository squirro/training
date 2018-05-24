# ML Data Setup / Loading

The scripts included here are used for setting up a sample data set to use for testing the machine learning service included with Squirro 2.6+

## Data set contents
The sample data set is a set of 10,000 fake people. Each record represents one person, and has a value of `first_name`, `last_name`, `age`, and `gender`.
A preview is shown below:

last_name|gender|first_name|age
--- | --- | --- |  ---
Harvey|M|Wayne|48
Walter|F|Jane|68
Horn|M|Robert|56
Thorne|M|Daniel|53
Tyler|F|Melissa|63

## Usage
To load this sample data set into squirro, first modify the file `load.sh` and add in your `cluster`, `token`, and `project_id` values in lines 3-5 of the file.

```bash
CLUSTER=...
TOKEN=...
PROJECT_ID=...
```
