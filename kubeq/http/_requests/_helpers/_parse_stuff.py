from dataclasses import dataclass
from box import Box

from kubeq.entities import KubeNames, KubeKind, KubeResource
from kubeq.entities._resource._sub_resource import KubeSubResource


@dataclass
class ResourceCtx:
    version: str
    group: str


def parse_names(resource: Box):
    return KubeNames(
        main=resource.singularResource,
        plural=resource.resource,
        short=tuple(resource.get("shortNames", [])),
    )


def parse_kind(kind: Box, ctx: ResourceCtx):
    return KubeKind(
        group=kind.group or ctx.group or "",
        version=kind.version or ctx.version or "v1",
        name=kind.kind,
    )


def parse_subresource(res: Box, ctx: ResourceCtx):
    return KubeSubResource(
        kind=parse_kind(res.responseKind, ctx),
        name=res.subresource,
        verbs=tuple(res.get("verbs", [])),
        is_status=res.subresource == "status",
    )


def parse_resource(res: Box, ctx: ResourceCtx):
    raw_subresources = res.get("subresources", [])
    subresources: dict[str, KubeSubResource] = {
        subres.subresource: parse_subresource(subres, ctx)
        for subres in raw_subresources
    }
    daddy = KubeResource(
        names=parse_names(res),
        kind=parse_kind(res.responseKind, ctx),
        categories=tuple(res.get("categories", [])),
        is_namespaced=res.scope == "Namespaced",
        verbs=tuple(res.get("verbs", [])),
        kids=subresources,
    )
    for x in subresources.values():
        x.parent = daddy

    return daddy
