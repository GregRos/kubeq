import inspect
import kubernetes


kubernetes.config.load_kube_config()


class K(kubernetes.client.CoreV1Api):
    def __init__(self):
        super().__init__()

        # iterate over methods in CoreV1Api, and modify them to add a _requestTimeout=5 kwargs parameter
        # only for methods defined directly on K
        for name, method in get_class_methods(kubernetes.client.CoreV1Api).items():
            if "_requestTiemout" in (method.__doc__ or ""):
                setattr(
                    self,
                    name,
                    lambda *args, **kwargs: method(*args, **kwargs, _requestTimeout=5),
                )


k8s = K()
