---
title: "Training cifar10 on Polyaxon"
title_link: "Training cifar10"
meta_title: "Training cifar10 on Polyaxon - Tutorials"
meta_description: "Training cifar10 on Polyaxon."
featured: false
custom_excerpt: "Training cifar10 on Polyaxon. "
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - tutorials
    - training
---

Before training experiments, we need to have Kubernetes cluster and 2 persistent volume claims in ReadWriteMany mode for our data and outputs.


## Clone repo

Please clone the [Polyaxon examples repo](https://github.com/polyaxon/polyaxon-examples)

```bash
$ git clone https://github.com/polyaxon/polyaxon-examples.git
```


## Train experiments 

1. Change to examples folder, and specifically to cifar10

    ```bash
    $ cd /path/to/polyaxon-examples/tensorflow/cifar10
    ```

2. Deploy Polyaxon

    Add polyaxon charts to helm.

    ```bash
    $ helm repo add polyaxon https://charts.polyaxon.com
    $ helm repo update
    ```

    Now you can install Polyaxon with the `azure/polyaxon_config.yml` file,
    it overrides the default values from Polyaxon, by adding the data and outputs `existingClaim`
    with the values we just created. It also sets the compatible NVidia paths with azure GPU nodes.

    ```bash
    $ helm install polyaxon/polyaxon --name=polyaxon --namespace=polyaxon -f ../azure/polyaxon-config.yml
    ```

    If you get the following error message: `Error: incompatible versions client[v2.X.X] server[v2.X.X]`
    You should upgrade helm. Please run:

    ```bash
    $ helm init --upgrade
    ```

    And then try again to install polyaxon.

3. Configure Polyaxon-CLI

    When the deployment is finished, you will receive a list of instructions in order to configure the cli.

4. Login with the superuser created by Polyaxon

    the instructions will tell you the superuser's username and a command to get the password.

    ```bash
    $ polyaxon login --username=root --password=rootpassword
    ```

5. Create a project

    ```bash
    $ polyaxon project create --name=cifar10 --description='Train and evaluate a CIFAR-10 ResNet model on polyaxon'
    ```

6. Init the project

    ```bash
    $ polyaxon init cifar10
    ```

7. Create the first experiment

    Unless you copied the data manually to the data share create in the previous section,
    the first time you create an experiment, it will create the data.

    Start an experiment with the default `polyaxonfile.yml`

    ```bash
    $ polyaxon run -u
    ```

8. Watch the logs

    ```bash
    $ polyaxon experiment -xp 1 logs

      Building -- creating image -
      master.1 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/1', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      master.1 --   force_gpu_compatible: true
      master.1 -- }
    ```

9. Watch the resources

    When the experiment starts training, you can also watch the logs

    ```bash
    $ polyaxon experiment -xp 1 resources

      Job       Mem Usage / Limit    CPU% - CPUs
    --------  -------------------  ---------------
    master.1  1.26 Gb / 6.79 Gb    120.11% - 6
    ```

    N.B. Azure seems to have an issue with reporting docker cpu resources.

10. Run a distributed experiment

    ```bash
    $ polyaxon run -f polyaxonfile_distributed.yml -u
    ```


8. Watch the logs

    ```bash
    $ polyaxon experiment -xp 2 logs

      Building -- creating image -
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_3/: (?, 16, 16, 32)
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_4/: (?, 16, 16, 32)
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_5/: (?, 16, 16, 32)
      worker.3 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/2', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      worker.3 --   force_gpu_compatible: true
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_6/: (?, 16, 16, 32)
      worker.3 -- }
      worker.3 -- allow_soft_placement: true
      worker.3 -- , '_tf_random_seed': None, '_task_type': None, '_environment': 'local', '_is_chief': True, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7fc7e9f53850>, '_tf_config': gpu_options {
      worker.3 --   per_process_gpu_memory_fraction: 1.0
      worker.3 -- }
      worker.3 -- , '_num_worker_replicas': 0, '_task_id': 0, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_evaluation_master': '', '_keep_checkpoint_every_n_hours': 10000, '_master': '', '_log_step_count_steps': 100}
      master.1 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/2', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      master.1 --   force_gpu_compatible: true
      master.1 -- }
      ...
      worker.2 -- INFO:tensorflow:Evaluation [2/100]
      worker.4 -- INFO:tensorflow:Evaluation [2/100]
      worker.2 -- INFO:tensorflow:Evaluation [3/100]
      worker.4 -- INFO:tensorflow:Evaluation [3/100]
      worker.2 -- INFO:tensorflow:Evaluation [4/100]
      worker.4 -- INFO:tensorflow:Evaluation [4/100]
      worker.2 -- INFO:tensorflow:Evaluation [5/100]
      worker.4 -- INFO:tensorflow:Evaluation [5/100]
      worker.2 -- INFO:tensorflow:Evaluation [6/100]
      worker.4 -- INFO:tensorflow:Evaluation [6/100]
      worker.2 -- INFO:tensorflow:Evaluation [7/100]
      worker.4 -- INFO:tensorflow:Evaluation [7/100]
      worker.2 -- INFO:tensorflow:Evaluation [8/100]
      worker.4 -- INFO:tensorflow:Evaluation [8/100]
      worker.2 -- INFO:tensorflow:Evaluation [9/100]
      worker.4 -- INFO:tensorflow:Evaluation [9/100]
    ```

9. Watch the resources

    When the experiment starts training, you can also watch the logs

    ```bash
    $ polyaxon experiment -xp 2 resources

    Job       Mem Usage / Total    CPU% - CPUs
    --------  -------------------  -------------
    master.1  1.23 Gb / 55.03 Gb   0.01% - 6
    worker.2  1.1 Gb / 6.79 Gb     73.33% - 2
    worker.3  1.26 Gb / 55.03 Gb   246.32% - 6
    worker.4  1.12 Gb / 6.79 Gb    67.03% - 2
    ps.5      1.21 Gb / 55.03 Gb   272.41% - 6
    ```

10. Run an experiment with GPU

    ```bash
    $ polyaxon run -f polyaxonfile_gpu.yml -u
    ```

11. Watch the logs

    ```bash
    $ polyaxon experiment -xp 3 logs

    master.1 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/3', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
    master.1 --   force_gpu_compatible: true
    master.1 -- }
    master.1 -- allow_soft_placement: true
    master.1 -- , '_tf_random_seed': None, '_task_type': None, '_environment': 'local', '_is_chief': True, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7fd2638d9490>, '_tf_config': gpu_options {
    master.1 --   per_process_gpu_memory_fraction: 1.0
    ...
    ```

12. Watch the resources


    ```bash
    $ polyaxon experiment -xp 3 resources

    Job       Mem Usage / Limit    CPU% - CPUs
    --------  -------------------  -------------
    master.1  1.57 Gb / 55.03 Gb   80.91% - 6
    ```

    Since this experiment is running with GPU, we can also watch the GPU metrics

    ```bash
    $ polyaxon experiment -xp 3 resources --gpu

    job_name    name         GPU Usage  GPU Mem                GPU Temperature    Power Draw    Power Limit
    ----------  ---------  -----------  -------------------- -----------------  ------------  -------------
    master.1    Tesla K80           75  10.71 Gb / 11.17 Gb                 69           125            149
    ```
