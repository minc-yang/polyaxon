---
title: "Setup helm"
title_link: "Setup helm"
meta_title: "Setup helm - Guide"
meta_description: "Polyaxon uses Helm to install and manage a deployment on Kubernetes."
featured: true
custom_excerpt: "Polyaxon uses Helm to install and manage a deployment on Kubernetes."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - guides
    - helm
    - kubernetes
---

[Helm](https://helm.sh/) is the official package manager for Kubernetes,
it's a useful tool to install, upgrade, and manage applications on a Kubernetes cluster.

You will be using Helm to install and manage Polyaxon on your cluster.

## Install Helm

The simplest way to install helm is to run Helm’s installer script at a terminal:

```bash
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
```

## Initialize Helm and grant RBAC

After installing helm on your machine, initialize helm on your Kubernetes cluster
(you can check the [instruction provided by helm](https://github.com/kubernetes/helm/blob/master/docs/rbac.md)).

Run the commands:

```bash
$ kubectl --namespace kube-system create sa tiller
$ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
```

```bash
$ helm init --service-account tiller
```

This is only needed once per Kubernetes cluster.


## Verify Helm version

You can check that the Helm installed is compatible with Polyaxon

```bash
$ helm version
```

Make sure you have at least version 2.5!

## Upgrade Helm

If you need to upgrade helm, you can run the following command

```bash
$ helm init --upgrade
```
