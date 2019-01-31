---
title: "Projects"
sub_link: "projects"
meta_title: "Projects in Polyaxon - Core Concepts"
meta_description: "A Project in Polyaxon is very similar to a project in github, it aims at organizing your efforts to solve a specific problem."
tags:
    - concepts
    - polyaxon
    - experimentation
    - projects
    - architecture
sidebar: "concepts"
---

A `Project` in Polyaxon is very similar to a project in github,
it aims at organizing your efforts to solve a specific problem.

## Create a project

To create a project, you can both use the Polyaxon Dashboard or the Polyaxon CLI.

The projects consist of a required argument `--name` an optional argument `--description`,
and a flag `--private` with a default value set to `False`.

The projects could be `public` (default behaviour) or `private`,
in that case only you i.e. `logged-in user`, and `superusers` can access the project.

Public projects are visible to everyone as read only mode, and read/write mode to the `owner` and `superusers`.

> More permissions and roles are available for organization who want to reflect their structure in the EE version.


> Tip "Only the creator and superusers can create experiment groups and experiments"
Even if you set your project to `public`, only you, i.e. the `owner`, and the `superusers`, 
will be able to run experiments in this project. `public` only gives read access to other users in your team.


```bash
$ polyaxon project create --name=mnist --description='Classification of handwritten images.'
```

> For more details about this command please run `polyaxon project create --help`, 
or check the [command reference](/references/polyaxon-cli/project/#create)

The project is created by default `public`, to make it private please add `--private`

## Initializing a project

After creating a project, you can start your experimentation process,
and the first step is to initialize a workspace for your project on your workstation.

```bash
$ mkdir mnist
$ cd mnist

$ polyaxon init mnist

Project `mnist` was initialized and Polyaxonfile was created successfully `polyaxonfile.yml`
```

When a project is initialized, polyaxon creates a default `.polyaxonignore`,
you can customize it to ignore the files that you don't want to upload.

Now you can add some code to your project.

Before doing anything you must update the default polyaxonfile to tell polyaxon how to run your code

```bash
$ vi polyaxonfile.yml
```

## Upload code for this project

Create the code you wish to run on Polyaxon, e.g.

```bash
$ vi train.py
...
```

Upload the code to polyaxon to commit this current version.

```bash
$ polyaxon upload
[================================] 675/675 - 00:00:00

Files uploaded.
```


You are ready now to run experiments, please go to [experiment groups](/concepts/experiment-groups/)
if you want to run multiple experiments concurrently and perform hyperparameters search.
Otherwise go to [experiments](/concepts/experiments/) if you want to run a single experiment.
