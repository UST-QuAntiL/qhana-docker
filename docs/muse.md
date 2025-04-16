# Using the MUSE dataset

The docker compose setup includes a subset of the MUSE dataset.
This "Mini MUSE" dataset can be used to showcase a more complicated experiment flow.

## Using the Mini MUSE dataset

```{warning}
Work in Progress.
```

```
TODO: purpose and goal of this experiment for reference
TODO: subsections
```
### Creating the experiment

First create a new experiment by clicking on the "New Experiment" button in the [Experiments](http://localhost:8080/#/) tab.
Fill out the dialog and submit it. This will automatically open the new experiment.

<image 1>

### Loading the dataset

To import the Mini MUSE dataset, we use the "Costume Loader" plugin.
Navigate to the "Workspace" tab and select the "Costume Loader" plugin.
Enter the following parameters in the plugin UI:
- DB host: `muse-db`
- DB user name: `test`
- DB password: `test`
- DB database: `KostuemRepo`
Start the plugin by clicking "submit".

<image 2>

After submitting, the QHAna UI shows the experiment step in the "Timeline" tab.
In the overview of the timeline step, we can verify the success of the plugin execution.
Furthermore, in the "Outputs" tab of the timeline step we can inspect plugin output.

<image 3>

Now we can begin processing the data.
First we use the "Wu Palmer similarities" plugin to calculate the semantic similarities between the entities of the dataset.
Navigate to the "Workspace" tab and use the search bar to find the "Wu Palmer similarities" plugin.
Select it and choose the previously created files as input for the plugin by clicking the "choose file" button next to the "Entities URL" input field.
This opens a dialog which lists suitable input files.
Select the JSON file containing the entities and click "Choose".
Similarly you can choose the attribute metadata and the taxonomies of the dataset in the second and third input field.

<image 4>

In the "Attributes" input field, enter the list of attributes for which the semantic similarity is to be calculated.
In this tutorial we use the following attributes:

```bash
dominanteFarbe
dominanterZustand
dominanteCharaktereigenschaft
dominanterAlterseindruck
genre
```

<image 5>

Once all inputs are entered, click "Submit" to start the plugin execution.
The UI then shows the "Timeline" tab, in which we can verify the success of the experiment step.
The plugin output is a zip-file containing the element similarities.
We can now use the "Sym Max Mean attibute comparer" plugin to calculate the attribute similarities from the element similarities.
Select the plugin in the "Workspace" tab and choose the files of the entities and the element similarities in the corresponding input fields.
In the attributes field, enter the same set of attributes used in the previous plugin.

```{tip}
If you don't remember which attributes you used to calculate the element similarities, you can find out in the "Timeline" tab.
Click the timeline step in which the "Wu Palmer" plugin was executed and switch to the "Inputs" tab.
In this tab you can find a table that lists the chosen input values for the plugin execution.
Here you can copy the value of the "attributes" parameter to reuse it for the next plugins.
```


### Visualizing the results


```{todo}
Update the mini muse workflow description.
```

If you have started QHAna together with the Mini MUSE database, you can take a look at the following documents on how to process the data with the available plugins.

Plugin sequence: {download}`PDF <pdfs/Mini_MUSE_Plugin_Sequence.pdf>`

Tutorial with screenshots: {download}`PDF <pdfs/Mini_MUSE_Plugin_Tutorial.pdf>`

## Using the NISQ-Analyzer plugin

On a fresh start, the "nisq-analyzer" plugin will display no implementations.

![NISQ_Analyzer plugin with no implementations.](images/nisq-analyzer-empty.png)

To add implementations, you have to run a plugin that produces a `.qasm` file as output.
For example you can follow the "MUSE plugin sequence" mentioned above.
Or you can use the "file-upload" plugin to upload a local `.qasm` file.

![File Upload plugin.](images/nisq-analyzer-upload-file.png)

The the "nisq-analyzer" plugin will display this implementation and you can use it like the standalone [NISQ-Analyzer](https://github.com/UST-QuAntiL/nisq-analyzer).

![NISQ-Analyzer plugin with one implementation.](images/nisq-analyzer-one-implementation.png)
