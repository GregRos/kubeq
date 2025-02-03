class ListRequest:
    def __init__(self, kind: str, field_selector: dict[str, str], label_selector: str):
        self.kind = kind
        self.field_selector = field_selector
        self.label_selector = label_selector
