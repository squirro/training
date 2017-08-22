# Using custom plugins for the Squriro Data Loader in the frontend

### NOTE: Uploading plugins requires Squirro Version 2.5.0 or later. For users running Squirro version 2.4.X, it is recommended to use the Data Loader from the command line only

This example shows how custom plugins can be created for the Squirro Data Loader, and used within the Squirro web UI. As long as a few rules are followed, any plugin can be uploaded to Squirro and used within the UI.
Once uploaded, the plugin will appear in the UI as shown below:

![alt text](https://lh5.googleusercontent.com/oxsG1i-fx3Dv-07kvtDbD4WJPjXk7NmCZdY1-CRbwXqLuJXq6Uh46gYPtblYHICEe6r9xBcNigfmK2c=w2560-h1958-rw "An uploaded Plugin")

## Plugin Design
Compared to designing a plugin to work with the Squirro Data Loader via the command line, there are a few more rules which must be followed.

### Requirements for the plugin
Any additional python packages required by the data loader plugin should be included in a `requirements.txt` file within the folder for the data loader plugin. Each of these requirements will be installed using `pip` when the plugin is uploaded to Squirro.

If no there are no additional requirements for the plugin, the `requirements.txt` file can be empty.

### The dataloader_plugin.json file
All Data loader plugins are uploaded by the `squirro_asset` tool. This tool looks for a file called `dataloader_plugin.json` within the folder for the data loader plugin. The `dataloader_plugin.json` file tells the `squirro_asset` tool how to upload the plugin, and which files and resources are needed.

An example of a `dataloader_plugin.json` file is shown below
```json
{
    "title": "Fake Post Data",
    "description": "Load Lorem Ipsum Post data into Squirro",
    "plugin_file": "post_plugin.py",
    "requirements_file": "requirements.txt",
    "category": "developers",
    "thumbnail_file": "post.png"
}
```

### Plugin Icons
If desired, icons can be included for plugins, which are shown next to the plugin in the UI. For this plugin, we will use the icon `post.png` which is included here.
For best results, icons should always be included in PNG with a square (1:1) aspect ratio.

## Uploading the Plugin
To upload a plugin to Squirro, the `squirro_asset` tool within the toolbox should be used.
The `squirro_asset` tool must be run from _outside_ the data loader plugin folder, so that the plugin folder can be referenced as an argument. For this reason, the `upload.sh` script that we have will back out a directory before running the upload command.
