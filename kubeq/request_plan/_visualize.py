import yaml
from kubeq.request_plan._request_plan import RequestPlan
from rich.syntax import Syntax
from rich.console import Console

c = Console()


def visualize(plan: RequestPlan):
    d = plan.to_dict_desc()
    as_yaml = (
        yaml.dump(d, default_style=None, sort_keys=False)
        .replace("^1", "@")
        .replace("^2", "%")
    )
    syntax = Syntax(
        as_yaml,
        "yaml",
        theme="monokai",
    )
    c.print(syntax)
