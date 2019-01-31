---
title: "Jobs"
sub_link: "jobs"
meta_title: "jobs in Polyaxon - Core Concepts"
meta_description: "A Job is the execution of your code to do some data processing or any generic operation."
tags:
    - concepts
    - polyaxon
    - experimentation
    - jobs
    - architecture
sidebar: "concepts"
---
Assuming that you have already a [project](/concepts/projects/) created and initialized,
and you uploaded your code containing a file `prepare_data.py` that does some preprocessing of your data.
Of course you can call this file directly from your experiments, but that will lead to basically
doing the same operation for all experiments.

## Updating the polyaxonfile.yml

Running a job is very similar to running an experiment, in the sense that you need to have a polyaxonfile and code to run.

The polyaxonfile will define the environment requirements needed to run your job.

```yaml
---
...

build
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 prepare_data.py
```

> For more details about the `run section` check the [run section reference](/polyaxonfile_specification/sections#run)


## Running a job

To run this polyaxonfile execute

```bash
$ polyaxon run -f my_polyaxonfile.yml

Job 1 was created.
```

> For more details about this command please run `polyaxon run --help`, 
or check the [command reference](/references/polyaxon-cli/run/)

## Checking the jobs of a project

We can check that the project has now a job created.
For that we can use Polyaxon dashboard or Polyaxon CLI,

```bash
$ polyaxon project jobs
```

> For more details about jobs, please run `polyaxon job --help`,
or check the [command reference](/references/polyaxon-cli/job/)
