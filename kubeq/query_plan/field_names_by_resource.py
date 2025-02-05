from re import M

fields_by_resource = {
    "Pod": [
        "spec.nodeName",
        "spec.restartPolicy",
        "spec.schedulerName",
        "spec.serviceAccountName",
        "spec.hostNetwork",
        "status.phase",
        "status.podIP",
        "status.nominatedNodeName",
    ],
    "Event": [
        "involvedObject.kind",
        "involvedObject.namespace",
        "involvedObject.name",
        "involvedObject.uid",
        "involvedObject.apiVersion",
        "involvedObject.resourceVersion",
        "involvedObject.fieldPath",
        "reason",
        "reportingComponent",
        "source",
        "type",
    ],
    "Secret": [
        "type",
    ],
    "Namespace": [
        "status.phase",
    ],
    "ReplicaSet": [
        "status.replicas",
    ],
    "ReplicationController": [
        "status.replicas",
    ],
    "Job": ["status.successful"],
    "Node": [
        "spec.unschedulable",
    ],
    "CertificateSigningRequest": [
        "status.signerName",
    ],
}
