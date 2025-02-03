from attr import dataclass


def expand_field(name: str):
    match name:
        case "n":
            return "metadata.name"
        case "ns":
            return "metadata.namespace"
        case _:
            return name


def expand_label(name: str):
    match name:
        case "a":
            return "app"
        case _:
            return name


def split_to_selector_types(s: list[str]):
    all_separated = [x.strip() for w in s for x in w.split(",")]

    labels = {}
    fields = {"status.phase": "Running"}
    container = {}
    for w in all_separated:
        if w.startswith("^"):
            container["name"] = w[1:]
            continue
        target = fields
        if w.startswith("[") and w.endswith("]"):
            w = w[1:-1]
            target = labels

        k, v = split_kvp(w)
        target[k] = v
    return labels, fields, container


def split_kvp(s: str):
    all = s.split("=", 1)
    if len(all) == 1:
        raise ValueError(f"Invalid selector: {s}")
    [k, v] = all
    return expand_label(k), v


@dataclass
class Selectors:
    label_selector: str
    field_selector: str
    container_selector: dict[str, str] | None = None


def rephrase_selectors(s: list[str]):
    labels, fields, container = split_to_selector_types(s)
    return Selectors(
        label_selector=",".join([f"{k}={v}" for k, v in labels.items()]),
        field_selector=",".join([f"{k}={v}" for k, v in fields.items()]),
        container_selector=container if container else None,
    )
