from typing import Dict, List, Tuple

from hestia.datetime_typing import AwareDT

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from constants.k8s_jobs import JOB_NAME_FORMAT, TENSORBOARD_JOB_NAME
from db.models.abstract_jobs import AbstractJobStatus, JobMixin
from db.models.outputs import OutputsRefsSpec
from db.models.plugins import PluginJobBase
from db.models.unique_names import TENSORBOARD_UNIQUE_NAME_FORMAT
from libs.paths.jobs import get_job_subpath
from libs.spec_validation import validate_tensorboard_spec_config
from schemas.specifications import TensorboardSpecification


class TensorboardJob(PluginJobBase, JobMixin):
    """A model that represents the configuration for tensorboard job."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs')
    config = JSONField(
        help_text='The compiled polyaxonfile for the tensorboard job.',
        validators=[validate_tensorboard_spec_config])
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    status = models.OneToOneField(
        'db.TensorboardJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    @cached_property
    def unique_name(self) -> str:
        return TENSORBOARD_UNIQUE_NAME_FORMAT.format(
            project_name=self.project.unique_name,
            id=self.id)

    @cached_property
    def subpath(self) -> str:
        return get_job_subpath(job_name=self.unique_name)

    @cached_property
    def pod_id(self) -> str:
        return JOB_NAME_FORMAT.format(name=TENSORBOARD_JOB_NAME, job_uuid=self.uuid.hex)

    @cached_property
    def specification(self) -> 'TensorboardSpecification':
        return TensorboardSpecification(values=self.config)

    @property
    def has_specification(self) -> bool:
        return self.config is not None

    def set_status(self,  # pylint:disable=arguments-differ
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   details: Dict = None) -> bool:
        return self._set_status(status_model=TensorboardJobStatus,
                                created_at=created_at,
                                status=status,
                                message=message,
                                traceback=traceback,
                                details=details)

    def get_absolute_outputs_paths(self) -> str:
        import stores

        if self.experiment:
            return stores.get_experiment_outputs_path(
                persistence=self.experiment.persistence_outputs,
                experiment_name=self.experiment.unique_name,
                original_name=self.experiment.original_unique_name,
                cloning_strategy=self.experiment.cloning_strategy)

        if self.experiment_group:
            return stores.get_experiment_group_outputs_path(
                persistence=self.experiment_group.persistence_outputs,
                experiment_group_name=self.experiment_group.unique_name)

        return stores.get_project_outputs_path(
            persistence_outputs=None,
            project_name=self.project.unique_name)

    def get_named_outputs_paths(self) -> Tuple[List, str]:
        import stores

        def get_named_experiment_outputs_path(experiment):
            persistence = experiment.persistence_outputs
            outputs_path = stores.get_experiment_outputs_path(
                persistence=persistence,
                experiment_name=experiment.unique_name,
                original_name=experiment.original_unique_name,
                cloning_strategy=experiment.cloning_strategy)
            tensorboard_path = '{}:{}'.format(
                experiment.unique_name,
                outputs_path)
            return [OutputsRefsSpec(path=outputs_path, persistence=persistence)], tensorboard_path

        if self.experiment:
            return get_named_experiment_outputs_path(self.experiment)

        if self.experiment_group:
            experiments = self.experiment_group.group_experiments.all()
        else:
            experiments = self.project.experiments.all()

        outputs_specs = []
        tensorboard_paths = []
        for experiment in experiments:
            outputs_spec, tensorboard_path = get_named_experiment_outputs_path(experiment)
            outputs_specs += outputs_spec
            tensorboard_paths.append(tensorboard_path)

        return outputs_specs, ','.join(tensorboard_paths)

    @cached_property
    def outputs_path(self) -> str:
        return self.get_named_outputs_paths()


class TensorboardJobStatus(AbstractJobStatus):
    """A model that represents tensorboard job status at certain time."""
    job = models.ForeignKey(
        'db.TensorboardJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Tensorboard Job Statuses'
