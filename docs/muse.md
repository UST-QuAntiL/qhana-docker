# Using the MUSE dataset

The docker compose setup includes a subset of the MUSE dataset.
This "Mini MUSE" dataset can be used to showcase a more complicated experiment flow.

## Using the Mini MUSE dataset

The MUSE dataset contains a set of movie costumes.
Each entity in the dataset corresponds to a costume.
The attributes of the entity describe the context and the details of the costume.

In this experiment we analyze the costumes of the Mini MUSE dataset.
The goal of this experiment is to calculate clusters of similar costumes and to visualize the clusters in a plot.
This allows us to see patterns and similarities among movie costumes using machine learning.

### Creating the experiment

First navigate to the "Experiments" tab.
Do this by opening the [QHAna UI](http://localhost:8080/#/) or by clicking the QHAna logo in the top left corner.
Create a new experiment by clicking on the "New Experiment" button.
Fill out the dialog and submit it. This will automatically open the new experiment.

![The experiment creation dialog.](images/muse-workflow-create-experiment.png)

### Loading the dataset

To import the Mini MUSE dataset, we use the "Costume Loader" plugin.
Navigate to the "Workspace" tab and select the "Costume Loader" plugin.
Enter the following parameters in the plugin UI:
- DB host: `muse-db`
- DB user name: `test`
- DB password: `test`
- DB database: `KostuemRepo`

Start the plugin by clicking "submit".

![The filled in "Costume Loader" plugin UI.](images/muse-workflow-costume-loader-inputs.png)

After submitting, the QHAna UI shows the experiment step in the "Timeline" tab.
In the overview of the timeline step, we can verify the success of the plugin execution.
Furthermore, in the "Outputs" tab of the timeline step we can inspect plugin output.

![The finished result of the "Costume Loader" plugin.](images/muse-workflow-costume-loader-timeline-step.png)

### Processing the data

Now that the dataset is successfully imported, we can begin processing the data.
First, we use the "Wu Palmer similarities" plugin to calculate the semantic similarities between the entities of the dataset.
Navigate to the "Workspace" tab and use the search bar to find the "Wu Palmer similarities" plugin.
Select it and choose the previously created files as input for the plugin by clicking the "choose file" button next to the "Entities URL" input field.
This opens a dialog which lists suitable input files.
Select the JSON file containing the entities and click "Choose".
Similarly, we can choose the attribute metadata and the taxonomies of the dataset in the second and third input field.

```{Note}
QHAna plugins exchange data using specific data types and serialization formats.
Each plugin defines the required format for its input and output data.
In the "Choose data" dialog, you can see the accepted format for the chosen input field.
For instance, the "Entities URL" input field of the "Wu Palmer similarities" plugin accepts files of the data type "entity/list", serialized as either JSON or CSV.
When executing a sequence of plugins, ensure that the input data type and serialization format are compatible with the output from the preceding plugins.
Note that we can only run the "Wu Palmer similarities" plugin, because its inputs match the outputs of the previously executed "Costume Loader" plugin.
```

![The "Choose data" dialog.](images/muse-workflow-wu-palmer-choose-file-dialog.png)

In the "Attributes" input field, enter the list of attributes for which the semantic similarity is to be calculated.

```{tip}
By clicking "show preview" below the "Entities URL" input field, you can open a preview of the entities below the input fields.
You can then scroll down and inspect the JSON file.
Here you can pick and copy attributes for the "Attributes" input field.
```

In this tutorial we use the following attributes:

```bash
dominanteFarbe
dominanterZustand
dominanteCharaktereigenschaft
dominanterAlterseindruck
genre
```

![The filled in "Wu Palmer similarities" plugin UI.](images/muse-workflow-wu-palmer-inputs.png)

Once all inputs are entered, click "Submit" to start the plugin execution.
The UI then shows the "Timeline" tab, in which we can verify the success of the experiment step.
The plugin output is a ZIP file containing the element similarities.
We can now use the "Sym Max Mean attibute comparer" plugin to calculate the attribute similarities from the element similarities.
Select the plugin in the "Workspace" tab and choose the files of the entities and the element similarities in the corresponding input fields.
In the "Attributes" field, enter the same set of attributes used in the previous plugin.

```{tip}
If you don't remember which attributes you used to calculate the element similarities, you can find out in the "Timeline" tab.
Click the timeline step in which the "Wu Palmer" plugin was executed and switch to the "Inputs" tab.
In this tab you can find a table that lists the chosen input values for the plugin execution.
Here you can copy the value of the "attributes" parameter to reuse it for the next plugins.
```

![The filled in "Sym Max Mean attribute comparer" plugin UI.](images/muse-workflow-sym-max-mean-inputs.png)

Start the plugin by clicking "submit".
The output of this plugin is a ZIP file containing the attribute similarities.
In the next step we use the "Similarities to Distances Transformers" plugin to get the attribute distances.
Switch to the "Workspace" tab and select the plugin.
Choose the file that contains the attribute similarities in the corresponding input field.
In the "Attributes" field, enter the same set of attributes once again.
In the "Transformer" field, we will keep the default option "Linear Inverse".

![The filled in "Similarities to distances transformers" plugin UI.](images/muse-workflow-similarities-to-distances-inputs.png)

After successful plugin execution, we have the attribute distances.
We can now use the "Aggregators" plugin to calculate the entity distances.
Select the plugin and choose the file containing the attribute distances in the input field.
We keep the default options for the remaining two input fields.

![The filled in "Aggregators" plugin UI.](images/muse-workflow-aggregators-inputs.png)

Upon submission, the plugin will generate a JSON file which contains the entity distances.
The entity distances can be converted to points in space using the "Multidimensional Scaling (MDS)" plugin.
Select the plugin in the Experiment Workspace and choose the file that contains the entity distances in the corresponding input field.
For the remaining input fields, we keep the default options.

![The filled in "Multidimensional Scaling (MDS)" plugin UI.](images/muse-workflow-mds-inputs.png)

After submitting, the plugin creates a JSON file containing the calculated entity points.
We can already inspect the results by switching to the "Outputs" tab in the timeline step.
In the "Preview With:" field, select "Clustered Scatter Plot Visualization" to visualize the entity points.
Note that results may vary, as MDS is not deterministic.

![The preview of the "Multidimensional Scaling (MDS)" plugin output.](images/muse-workflow-mds-output-preview.png)

Now the preprocessing is done and we can use a clustering plugin to group the data points.

```{tip}
In the "Workspace" tab, the search bar can also be used to search for plugins with certain plugin tags.
For instance, you can enter "clustering" to filter for clustering plugins.
```

For this tutorial we choose the "Classical k Means" plugin.
Choose the file containing the entity points as an input.
Tick the "Visualize" box to generate a HTML file displaying the clustered data.
Submitting creates two files:
The HTML file to visualize the clusters and a JSON file containing cluster labels for each entity.

![The filled in "Classical k Means" plugin UI.](images/muse-workflow-classical-k-means-inputs.png)

We can generate different results by processing the same data another time.
Now we use the "Classical k Medoids" plugin to process the same entity points once again.
To generate four clusters this time, change the parameter "Number of Clusters" to 4.
Upon submission, the plugin generates a JSON file with different labels for the entities.

![The filled in "Classical k Medoids" plugin UI.](images/muse-workflow-classical-k-medoids-inputs.png)

### Visualizing the results

To visualize the clusters, we can use the "Clustered Scatter Plot Visualization" plugin.
Select the plugin in the workspace and choose the JSON file containing the entity points in the corresponding input field.
This will automatically collapse the "Visualization Options" (i.e., the plugin input fields) to display a preview of the entity points.
Expand "Visualization Options" and choose one of the files that contain the cluster labels in the "Cluster URL" input field.
Since we used both the "Classical k Means" and the "Classical k Medoids", we have two options.
In this tutorial we will choose the file generated by the "Classical k Medoids".
Choosing the labels will show a preview of the entity points.
Now the entity points are colored according to their cluster labels.
To store the plot, expand "Visualization Options" once again and click "Submit".

![The preview shown in the "Clustered Scatter Plot Visualization" plugin UI.](images/muse-workflow-clustered-scatter-plot-preview.png)

We can find the stored plot in the "Data" tab among the other files generated by the plugins.
Enter "plot" in the search bar to filter for the plots of the clustered data.
In this experiment there are two plots:
The first one was generated when running the "Classical k Means" plugin, since we ticked the "Visualize" box before submitting.
The second one is the plot that we generated with the "Clustered Scatter Plot Visualization" plugin.

![The list of generated plots in the "Data" tab.](images/muse-workflow-experiment-data-page.png)

To export a plot, you can click "Download as File".
This will open a seperate tab in your browser in which the plot is displayed.
Clicking the small camera icon in the menu on the top right will download the plot as a PNG.
Alternatively, you can download that page as an HTML.

![The HTML page generated by the "Clustered Scatter Plot Visualization" plugin.](images/muse-workflow-cluster-plot.png)

## Using the NISQ-Analyzer plugin

On a fresh start, the "nisq-analyzer" plugin will display no implementations.

![NISQ_Analyzer plugin with no implementations.](images/nisq-analyzer-empty.png)

To add implementations, you have to run a plugin that produces a `.qasm` file as output.
For example you can follow the "MUSE plugin sequence" mentioned above.
Or you can use the "file-upload" plugin to upload a local `.qasm` file.

![File Upload plugin.](images/nisq-analyzer-upload-file.png)

The the "nisq-analyzer" plugin will display this implementation and you can use it like the standalone [NISQ-Analyzer](https://github.com/UST-QuAntiL/nisq-analyzer).

![NISQ-Analyzer plugin with one implementation.](images/nisq-analyzer-one-implementation.png)
