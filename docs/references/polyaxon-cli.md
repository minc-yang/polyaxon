---
title: "Polyaxon CLI"
sub_link: "polyaxon-cli"
meta_title: "Polyaxon Command Line Interface Specification - Polyaxon References"
meta_description: "Polyaxon Command Line Interface Specification."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
sidebar: "polyaxon-cli"
---

Polyaxon CLI is a tool and a client to interact with Polyaxon,
it allows you to manage your cluster, users, projects, and experiments.

## Installation

To install Polyaxon CLI please refer to the [installation documentation](/setup/cli/).


## Help

To get help from The Polyaxon CLI, you can run the following

```bash
$ polyaxon --help
```

To get help for any Polyaxon CLI Command, you can run the following

```bash
$ polyaxon command --help
```

## Commands References

 * [Auth](auth/)
 * [Check](check/)
 * [Config](config/)
 * [User](user/)
 * [Superuser role](superuser/)
 * [Init](init/)
 * [Project](project/)
 * [Upload](upload/)
 * [Run](run/)
 * [Experiment Group](experiment-group/)
 * [Experiment](experiment/)
 * [Job](job/)
 * [Build](build/)
 * [Dashboard](dashboard/)
 * [Tensorboard](tensorboard/)
 * [Notebook](notebook/)
 * [Cluster](cluster/)
 * [Bookmark](bookmark/)
 * [Version](version/)

## Caching

When using the Polyaxon CLI to run a command requiring a project, group, experiment, and/or a job,
you can always specify the values for these options, example:

 * `$ polyaxon project --project=user_1/project_10 get`
 * `$ polyaxon experiment --project=user_1/project_10 --experiment=2 get`
 * `$ polyaxon experiment --project=user_1/project_10 --experiment=3 --job=2 logs`
 * `$ polyaxon group --project=user_1/project_10 --group=2 experiments`


Polyaxon CLI allows also you to omit these options, i.e. project, experiment group, experiment, and job, the CLI does the following:

 1. When a username is missing, the username of the logged-in user is used.
 2. When a project name is missing, the name of the currently initialized project is used.
 3. When an experiment group, experiment, or job is missing, the last value is used.
 4. If no values are found, the CLI will show an error.

Some commands with caching:

 * `$ polyaxon project get`
 * `$ polyaxon experiment get`
 * `$ polyaxon group experiments`
 * `$ polyaxon job logs`
 * ...
