# Workflows

## Introduction

For developing serverless workflows to join together tasks to be run in a particular order. Define a workflow in JSON or YAML by stating the steps that need to be implemented. Deploy the workflow and it's ready to execute.
Workflows can use Secret Manager for storing keys for API calls. It has features including error handling, workflows within workflows (aka subworkflows) logical steps to cater for complex workflows.

## Orchestration vs. Choreography?

1. Orchestration - a central service manages the flow of communication between services. It's easier to modify and monitor and apply error handling.
2. Choreography - each service sends/receives events as needed. There's usually a central event broker to send messages, but it doesn't define or direct flow of communication. This enables truly independent services, but there is less traceable and manageability than orchestration.

Pub/Sub and Eventarc are both suited for choreography and event-driven services. Workflows is suited for centrally orchestrated services.

## A powerful orchestrator

Workflows is an orchestrator with many built-in features:
* Flexible retry and error handling between steps
* JSON parsing and variable passing
* Expression formulas and conditionsal execution
* Subworkflows and reuseable workflows
* Orchestration of services outside GCP
* Connectors to PubSub, Firestore, Cloud Functions, Cloud Run, Secret Manager, and more

[Blog post here!](https://cloud.google.com/blog/topics/developers-practitioners/better-service-orchestration-workflows)

__Note__ When using Secret Manager ensure the service account your workflow is using (default is the compute engine one) has the Secret Manager Secret Accesor role.

# How to Use

## Syntax

* Steps - Every workflow must have at least 1 step that's defined with an alphanumeric name and a colon
    * types - invoking HTTP endpoint, assigning a variable, sleeping, creating the logic for conditional jumps, returning a value
    * [detailed syntax on steps here](https://cloud.google.com/workflows/docs/reference/syntax#steps)
    * it seems workflows knows the type of Step based on the parameters provided. (e.g. An assign variable step will have a parameter `assign`. The sleep step will have the paramter `call` and value `sys.sleep` and then `args: sleep: [time_in_seconds]`)

* Calls - to call another function or expression. These can occur inside an expression. (e.g. `project: $(sys.get_env("google_cloud_project_ID")})`)
    * Calls can be either blocking or non-blocking. Blocking calls pause a workflow's execution as they have to be finished before the rest of the workflow can proceed
    * Blocking calls are - `http.*`, `sys.sleep`, `sys.log`, `googleapis.*`

* Jumps - control which step the workflow should execute next, including conditional jumps
    * Use `next` parameter
    * For conditional jump use `switch` defining the `condition` and `next` within it.
    * [example here](https://cloud.google.com/workflows/docs/reference/syntax#jumps)

```yaml
- getCurrentTime:
    call: http.get
    args:
      url: https://us-central1-workflowsample.cloudfunctions.net/datetime
    result: currentTime
- conditionalSwitch:
    switch:
      - condition: ${currentTime.body.dayOfTheWeek == "Friday"}
        next: friday
      - condition: ${currentTime.body.dayOfTheWeek == "Saturday" OR currentTime.body.dayOfTheWeek == "Sunday"}
        next: weekend
    next: workWeek
- friday:
    return: "It's Friday! Almost the weekend!"
- weekend:
    return: "It's the weekend!"
- workWeek:
    return: "It's the work week."
```

* Stop a workflow
    * use `next: end` to stop without requiring a return value 
    * or `return: ${variable_name}` to return a value, variable or expression

* Variables
    * store result by using `result: VARIABLE`
    * HTTP responses - when they are stored in a variable the JSON is converted to a dictionary. Workflows has built in parses for obtaining the data. Accessing fields can be done with the following syntax - `${VAR_NAME}.body|code.PATH_TO_FIELD)`
        * VAR_NAME = workflow variable that contains JSON response
        * body = to access body field of HTTP
        * code = to access HTTP response code
        * PATH_TO_FIELD = the path to obtaining desired field (remember fields are nested in json) - eg. `age_response.body.age` if the var name is age_response and the field required is age

* Arrays
    * Can be defined by a step - eg. the result of calling an HTTP request and storing it in a var
    * or in an assign step using `assign` - eg. `assign: - num_array['one', 'two']`
    * can iterate an array [look at example](https://cloud.google.com/workflows/docs/reference/syntax#arrays)

* Expressions - things evaluated by workflow engine and the output is used at time of execution, such as assigning the result to a var.
    * `${EXPRESSION}`
    * Can be used for conditional jumps, asigning vlaues to vars, HTTP request details, retry values, returning values
    * They cannot be use to make blocking calls (eg. `http.get` cannot be used)

* Runtime arguments - use the `params` field to create a named dictionary that can be later accessed. 

```yaml
main:
    params: [DICTIONARY_NAME]
    steps:
      - step1:
          return: ${DICTIONARY_NAME.PARAM_NAME}
```

* Data types - integer, double, string, boolean, null

* Dictionaries - can create dictionaries [see examples here](https://cloud.google.com/workflows/docs/reference/syntax#dictionaries)
    * Use expressions and dot notation to access content in a dict - eg `${myDict.Address.Coutnry}`

* Subworkflows - use `main` to indicate the main workflow, then have subworkflows defined and call a subworkflow from the main using the `call` field.

* Error Handling - raising exceptions, catching and handling HTTP request errors, retrying a failed step
    * eg. `raise: 'something went wrong'`
    * [read more on errors here](https://cloud.google.com/workflows/docs/reference/syntax#error_handling)
