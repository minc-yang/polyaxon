---
title: "Distributed Experiments"
sub_link: "distributed_experiments"
meta_title: "Distributed Experiments in Polyaxon - Core Concepts"
meta_description: "A Distributed Experiment is the execution of a model or a computation graph across a cluster."
tags:
    - concepts
    - polyaxon
    - experimentation
    - experiments
    - architecture
sidebar: "concepts"
---

Polyaxon supports and simplifies distributed training.

Depending on the framework you are using, you need to adapt your code to enable the distributed training,
and update your polyaxonfile with an environment section.

By default polyaxon creates a master job, so you only need to provide the workers and/or parameter servers.

To enable distributed runs, you need to update the [environment](/references/polyaxonfile-yaml-specification/sections/#environment) section.

The environment section allows to customize the resources of the master job,
as well as defining the topology of the experiment with a specific definition for each framework.

To customize the master resources, you just need to define the `resources` in the `environment` section, e.g.

```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1
```

Since the distributed training is performed differently by the different frameworks,
each subsection in this guide describes how to define the distributed training for each one of the supported frameworks.

## Distributed experiments with Tensorflow

To [distribute Tensorflow](https://www.tensorflow.org/deploy/distributed) experiment,
the user needs to define a cluster, which is a set of tasks that participate in the distributed execution.

Tensorflow defines 3 different types of tasks: master, worker, and parameter server.

To define a cluster in Polyaxon with a master, 3 workers, and 1 parameter server,
add a tensorflow subsection to the environment section of your polyaxonfile:

```yaml
...

environment:
  ...

  tensorflow:
    n_workers: 3
    n_ps: 1
```

You can have more control over the created tasks by defining the resources of each task
the same way we defined the resources for the master.

Here's an example where we define resources for the master, workers and parameter server.


```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1

  tensorflow:
    n_workers: 7
    n_ps: 3

    default_worker:
      resources:
        cpu:
          requests: 1
          limits: 2
        memory:
          requests: 256
          limits: 1024
        gpu:
          request: 1
          limits: 1

    worker:
      - index: 2
        resources:
          cpu:
            requests: 1
            limits: 2
          memory:
            requests: 256
            limits: 1024

    default_ps:
      resources:
        cpu:
          requests: 1
          limits: 1
        memory:
          requests: 256
          limits: 256

    ps:
      - index: 0
        resources:
          cpu:
            requests: 1
            limits: 1
          memory:
            requests: 512
            limits: 512
```

This configuration defines a cluster of 1 master, 7 workers, and 3 parameter servers.

The master's resources is defined in the resources section, i.e.

```yaml
resources:
  cpu:
    requests: 1
    limits: 2
  memory:
    requests: 256
    limits: 1024
  gpu:
    request: 1
    limits: 1
```

The third worker (worker with index == 2) has a specific resources definition:

```yaml
worker_resources:
  - index: 2
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
```
And all the other workers have the same default worker resources definition, i.e.

```yaml
default_worker:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1
```

Same logic applies to the parameter servers with the `default_ps.resources` and `ps_resources`.

## Distributed experiments with MXNet

In a similar fashion, [MXNet](https://mxnet.incubator.apache.org/faq/multi_devices.html#distributed-training-with-multiple-machines) defines 3 types of tasks: scheduler, workers, and parameter servers.

To define an MXNet cluster in Polyaxon with a scheduler, 3 workers, and 1 parameter server,
add an mxnet subsection to the environment section of your polyaxonfile:

```yaml
...

environment:
  ...

  mxnet:
    n_workers: 3
    n_ps: 1
```

You can customize the resources of each task the same way it was explained in the tensorflow section.


## Distributed experiments with Pytorch

[Distributed Pytorch](http://pytorch.org/tutorials/intermediate/dist_tuto.html) is also similar but only defines a master task (worker with rank 0) and a set of worker tasks.

To define a Pytorch cluster in Polyaxon with a master, 3 workers,
add a pytorch subsection to the environment section of your polyaxonfile:


```yaml
...

environment:
  ...

  pytorch:
    n_workers: 3
```

You can customize the resources of each task the same way it was explained in the tensorflow section.
