from ._get_resource_kinds import KubeGetResourceKinds
from ._get_resources import KubeGetResources

type KubeRequest = KubeGetResourceKinds | KubeGetResources
