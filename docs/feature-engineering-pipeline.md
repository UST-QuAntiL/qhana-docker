# Using the Feature Engineering Pipeline

The "Feature Engineering Pipeline" plugin turns a set of entities with taxonomy and
numeric attributes into a single feature vector per entity, which can then be used
for clustering or other machine learning tasks. It was built with the Muse4Music
dataset in mind, which describes music pieces using taxonomies (e.g. intrumentation, volume)
and numeric values (e.g. harmonic density). The pipeline routes each attribute through a
suitable sub-plugin pipeline (Wu-Palmer similarities, Mapping, One-Hot Encoding, or a numeric
value pipeline), optionally concatenates the resulting vectors and reduces their
dimensionality with a Principal Component Analysis (PCA) step.

To understand how the pipeline works, without the Muse4Music dataset neede, this guide uses
a small, self-contained "Animals" demo dataset instead.

## The demo dataset

The "Animals" demo dataset describes 16 animals (e.g. cow, lion, eagle, dolphin, shark)
using six attributes:

- `taxonomicClass` and `diet` are plain taxonomies (tree hierarchies which can be compared via their tree position).
- `habitat` and `activityTime` are flat taxonomies whose nodes additionally carry a
  mapping vector (e.g. average temperature and humidity for `habitat`) which can be compared.
- `weightKg` is a single numeric value per animal, `temperatureRangeC` is a
  numeric vector (value range: minimum and maximum tolerated temperature).

## Creating the experiment

As in the [MUSE workflow](muse.md), first navigate to the "Experiments" tab and
create a new experiment by clicking "New Experiment". Fill out the dialog and
submit it to open the new experiment.

## Loading the dataset

To load the demo dataset, use the "Demo data loader" plugin. Navigate to the
"Workspace" tab and select the "Demo data loader" plugin. It only has a single
"Dataset" input field; select "Animals (16 entities, 6 attributes)" and click "submit".

![The Demo Data Loader Plugin](images/feat-eng-pipeline-data-loader.png)

After submitting, verify the successful execution in the "Timeline" tab. The
plugin produces three files: the entity list, the attribute metadata, and a ZIP
file containing the taxonomies.

![The Demo Data Loader Plugin Result](images/feat-eng-pipeline-data-loader-result.png)

## The Feature Engineering Pipeline: Basic settings

Navigate to the "Workspace" tab and search and select the "Feature Engineering Pipeline"
plugin. Its first page is split into several sections:

- **Basic Data**: the "Entities URL", "Entities Attribute Metadata URL" and
  "Taxonomies URL" input fields. Use the "choose file" dialog to select the three
  outputs of the "Demo data loader" step here.
- **Transformer Settings**, **Wu-Palmer Settings**, **Mapping Settings** and
  **MDS Settings**: default settings for the sub-plugins used by the pipelines.
- **Vector Concatenation Settings** and **PCA Settings**: settings for combining
  and reducing the per-attribute vectors into one final feature vector.

> The settings on this page are **shared defaults for every attribute**. On the
next page, each attribute can override the Wu-Palmer, Mapping or MDS settings
individually. For this tutorial, we leave all of these shared defaults as they
are and only change the settings described below.

For this tutorial you have to change no other settings.
Feel free to test some other settings here.

![The Basic Data input on the first Feature Engineering Pipeline Plugin Page](images/feat-eng-pipeline-router-page-1.png)

Click on submit to get to the attribute selection page, where you can assign the attributes to the pipelines.

## Assigning attributes to a pipeline

The second page lists every taxonomy attribute with a dropdown of pipeline
options ("None", "Wu-Palmer", "One-Hot", "Mapping"). The dropdown already marks
one option as "(Recommended)" for each attribute, based on whether its taxonomy
carries mapping values or not. Here, you can simply keep the
recommended option. Numeric attributes are listed separately with an "Include"
checkbox instead of a dropdown.

For the demo dataset, use the following settings:

> TODO Add image for the settings

This guide does not go into the per-attribute Wu-Palmer, Mapping or MDS settings
panels - for the demo dataset, the shared defaults from the previous page work
well, so there is no need to open and change them individually.

Once all attributes are assigned, click "submit" to start the pipeline execution.
Depending on the number of sub-plugins involved, this may take a moment; you can
follow the progress in the "Timeline" tab.
> TODO That is wrong with the timeline tab. I want to explain how the logging explains what is happening.

## Visualizing the results without clustering

As in the MUSE workflow, we can inspect the pipeline output before doing any
clustering. Switch to the "Outputs" tab of the timeline step and find the final,
concatenated and PCA-reduced entity vector file. In the "Preview With:" field,
select "Clustered Scatter Plot Visualization". Since no cluster labels are chosen,
this shows a plain 3D scatter plot of the animals - already a good opportunity to
check whether the reduced vector still separates the expected animal groups.
> TODO update above section after verifying it in the UI (no cluster labels?)
>
> TODO Add one or two images

## Clustering the results

Now use a clustering plugin to group the animals. Select the "Classical k-Means"
plugin in the "Workspace" tab, choose the final entity vector file as input, and
set "Number of Clusters" to a value that matches the expected number of animal
groups in the dataset (e.g. **4**, for farm/grazing animals, land predators,
birds and marine animals - adjust if the resulting clusters do not look
meaningful). Tick the "Visualize" box to also generate an HTML plot.

> TODO add Image to that settings

After submitting, switch to the "Outputs" tab. As in the MUSE workflow, you will
find a JSON file with the cluster labels and, because "Visualize" was ticked, an
HTML file with the plot. Use "Clustered Scatter Plot Visualization" to preview the
labeled entity points, or open the HTML file to export the plot as an image.

> TODO Add Image and explain, that the cluster can differ (I think it can differ)

### Processing the data a second time

As in the MUSE workflow, we can process the same entity vectors again with a
different clustering plugin to compare results. Select the "Classical k-Medoids"
plugin, choose the same final entity vector file as input, and set "Number of
Clusters" to a different value (e.g. **3**, for a coarser grouping). Tick
"Visualize" again and submit.

> TODO Add settings image
>
> TODO delete this last paragraph? Not sure now.

Compare the two clustering results in the "Outputs" tab: depending on the number
of clusters chosen, the animal groups may split or merge differently, e.g. birds
and marine animals might be combined into a single cluster with fewer clusters.
