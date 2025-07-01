from clinic.models import Job, OperationType, Operation

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
    Job.DOCTOR:       list(OperationType.values()), #all ops. #type:ignore
    Job.WORKER:       [],
    Job.OTHER:        [],
    Job.ADMIN:        [],
}

def get_allowed_operations_for(worker):
    ops = JOB_PERMISSIONS.get(worker.job, [])
    return Operation.objects.filter(pk__in=ops)

# in views
# from .utils.permissions import get_allowed_operations_for

# @login_required
# def appointment_create(request, oid):
#     operation = get_object_or_404(Operation, id=oid)
#     worker    = get_object_or_404(Worker, user=request.user)
#     allowed_ops = get_allowed_operations_for(worker)

#     # other logical operations and form submition