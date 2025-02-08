from box import Box

from kubeq.entities import KubeNames, KubeKind, KubeSubResource, KubeResource


def parse_names(resource: Box):
    return KubeNames(
        main=resource.singularResource,
        plural=resource.resource,
        short=tuple(resource.get("shortNames", [])),
    )


def parse_kind(kind: Box):
    return KubeKind(
        group=kind.group,
        version=kind.version or "v1",
        name=kind.kind,
    )


def parse_subresource(res: Box):
    return KubeSubResource(
        name=res.subresource,
        kind=parse_kind(res.responseKind),
        verbs=tuple(res.get("verbs", [])),
    )


def parse_resource(res: Box):
    raw_subresources = res.get("subresources", [])
    subresources: dict[str, KubeSubResource] = {
        subres.subresource: parse_subresource(subres) for subres in raw_subresources
    }
    daddy = KubeResource(
        names=parse_names(res),
        kind=parse_kind(res.responseKind),
        categories=tuple(res.get("categories", [])),
        is_namespaced=res.scope == "Namespace",
        verbs=tuple(res.get("verbs", [])),
        kids=subresources,
    )
    for x in subresources.values():
        x.parent = daddy

    return daddy
