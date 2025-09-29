# Workflows

This tutorial will demonstrate how to model a simple workflow containing a QHAna plugin, deploy it as a plugin, and execute it.

## Workflow Editor

First, open the "Workflow Editor" plugin. Without anything selected, open the "General" category on the right-side panel and enter a name for the workflow. 

![Enter name of workflow.](images/workflow-editor/workflow_name.png)

Next, click on the QHAna button and then on "Update Configurations" to update the list of plugins available as QHAna service tasks.

![Update QHAna configurations.](images/workflow-editor/update_qhana.png)

Then, click on the start node and select the three-dot menu.

![Open three dot menu.](images/workflow-editor/add_user_task1.png)

Search for "User Task" and select it. This creates a task where the user can enter input for the following plugins.

![Select User Task.](images/workflow-editor/add_user_task2.png)

Optionally, enter a name for this task.

![Enter name.](images/workflow-editor/name_user_task.png)

Select the user task and click on the three-dot menu.

![Open three dot menu.](images/workflow-editor/add_qhana_task1.png)

Select "Task" to create a new task after the current one.

![Select Task.](images/workflow-editor/add_qhana_task2.png)

Click the wrench icon.

![Click wrench icon.](images/workflow-editor/add_qhana_task3.png)

You can either search for the plugin name or navigate through the list "QHAna Tasks" -> "QHAna Service Tasks".
Select the "hello-world" plugin to convert this task to the QHAna service task for the "hello-world" plugin.
You could also use the "CUSTOM" QHAna service task and enter the details manually.

![Select hello-world.](images/workflow-editor/add_qhana_task4.png)

Click on the hello-world task and on the thick circle to add the end node.

![Add end node.](images/workflow-editor/add_end_node.png)

Now, we will configure the tasks. Select the user input task and select the "Generated Task Forms" type in the forms category.

![Select "Generated Task Forms" as forms type in the user task.](images/workflow-editor/select_forms_type.png)

In the "Form fields" category, click on the plus to create a new field and add as ID "qouput.inputHelloWorld".
For QHAna tasks the "qouput." prefix is used for all process variables that will contain the output value of said QHAna task.
For the form we define here, however, it is not necessary, but we use it for consistency.

![Configure the form field.](images/workflow-editor/configure_form_field.png)

Click on the hello-world task and add an input with the plus icon. Use "qinput.inputStr" as the local variable name. "qinput." is the prefix for all plugin input variables, and "inputStr" is the name of the plugin input and must be equal to one of the plugin parameter names. Choose "Map" as the assignment type and add a new map entry. Use "qouput.inputHelloWorld" and "plain" as value. This will map the output variable of the user task to the input of the hello-world task and therefore forward the user input to the hello-world plugin.

![Configure hello-world input.](images/workflow-editor/configure_hello_world_input.png)

Add an output with "result.qoutput.helloWorldResult" as process variable name. The prefix "result." marks this variable as a workflow result and ".qoutput" as QHAna plugin output. Select "String or expression" as assignment type and "${output}" as value to assign the output of the plugin to the process variable.

![Configure hello-world output.](images/workflow-editor/configure_hello_world_output.png)

To transform this workflow into an executable workflow, click on the wrench icon to the right of the "Transformation" button and make sure only "DataFlow Transformation" and "QHAna Transformation" are active.
After the transformation the name of the workflow is appended with "_transformed" to indicated that it was already transformed, but you can change the name as shown in the beginning.

![Configure transformation.](images/workflow-editor/configure_transformation.png)

Click on "Transformation" and you will get the shown workflow as result.

![Transform workflow.](images/workflow-editor/transform.png)

This transformation will add an unnecessary output to the hello-world task that must be removed, otherwise, it will result in an error during execution.

![Delete unnecessary output.](images/workflow-editor/delete_output.png)

Now, we will deploy the workflow as a plugin by clicking on "Deploy Workflow" and "Deploy as Plugin."

![Deploy as plugin.](images/workflow-editor/deploy_as_plugin.png)

### Excursion: File outputs from previous steps as input

If a step has produced a file as output and you want to use it as input for a later step as input you have to create a input with "Map" assignment type.
In the map entries you have to specify a "from" key to define from which process variable you want the output file.
Then you can use multiple filters to specify which file exactly you want if the process variable contains multiple files.
You can filter by file name if you add a "name" key and add the name as value.
This filter supports glob notation e.g. you can use "*" to indicate zero or more arbitrary characters.
To filter by data type you can add a "dataType" key and add the data type as value.
The same applies to "contentType".

![Add file input.](images/workflow-editor/file_input.png)


## Workflow Plugin

Go back to the experiment workspace to find the plugin with your chosen workflow name and the suffix "_transformed" (if you didn't change it) in the plugin list and click on "submit" to execute the workflow.

![Start workflow.](images/workflow-editor/start_workflow.png)

Now, wait until the "User Input" task is executed. You will be prompted to input text. When done, click "submit."

![Submit user input.](images/workflow-editor/submit_user_input.png)

When the workflow has finished, you will see "SUCCESS" as the status.

![Workflow is finished.](images/workflow-editor/workflow_finished.png)
