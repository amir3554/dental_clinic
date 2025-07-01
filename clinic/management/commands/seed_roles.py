from django.core.management.base import BaseCommand
from django.db import transaction

from clinic.models import Worker, Operation, Role, Job, OperationType

JOB_PERMISSIONS = {
    Job.SECRETARY:    [],
    Job.NURSE:        [
        OperationType.PERIODICAL_CHECKING,
        OperationType.DENTAL_CLEANING,
    ],
    Job.TECHNICIAN:   [
        OperationType.PERIODICAL_CHECKING,
        OperationType.DENTAL_CLEANING,
        OperationType.DENTAL_FILLING,
    ],
    Job.DOCTOR:       list(OperationType.values), 
    Job.WORKER:       [],
    Job.OTHER:        [],
    Job.ADMIN:        [],
}

class Command(BaseCommand):
    help = "Seed Role table based on worker.job permissions"

    @transaction.atomic
    def handle(self, *args, **options):
        # نظّف الجدول أولًا
        Role.objects.all().delete()

        roles_to_create = []
        for worker in Worker.objects.all():
            perms = JOB_PERMISSIONS.get(worker.job, []) # type:ignore
            for op_value in perms:
                try:
                    operation = Operation.objects.get(pk=op_value)
                except Operation.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Operation {op_value} not found, skipping."
                    ))
                    continue
                roles_to_create.append(
                    Role(worker=worker, operation=operation)
                )

        Role.objects.bulk_create(roles_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(
            f"Created {len(roles_to_create)} Role entries."
        ))
