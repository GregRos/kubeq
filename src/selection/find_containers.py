from attr import dataclass
from ..init.kubernetes import k8s


def find_container(selectors_line: list[str]) -> str:
    from dictum.selection.rephrase_selectors import rephrase_selectors

    selectors = rephrase_selectors(selectors_line)
    results = k8s.list_pod_for_all_namespaces(
        label_selector=selectors.label_selector,
        field_selector=selectors.field_selector,
    )
    if len(results.items) == 0:
        raise ValueError(f"Selector {' '.join(selectors_line)} matched no pods")

    if len(results.items) > 1:
        raise ValueError(f"Selector {' '.join(selectors_line)} matched multiple pods")
    containers = [
        c_status.container_id.split("://")[1]
        for result_pod in results.items
        for c_status in result_pod.status.container_statuses
        if c_status.state.running
    ]
    if len(containers) == 0:
        raise ValueError(f"Pod {' '.join(selectors_line)} has no running containers")

    if len(containers) > 1:
        raise ValueError(
            f"Pod {' '.join(selectors_line)} has multiple running containers"
        )
    return containers[0]
