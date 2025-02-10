from dataclasses import dataclass


@dataclass
class VerbDef:
    name: str
    short: str
    emoji: str


verbs = {
    "get": VerbDef("get", "g", "🔍"),
    "list": VerbDef("list", "l", "📃"),
    "update": VerbDef("update", "u", "✍️"),
    "create": VerbDef("create", "c", "🌱"),
    "delete": VerbDef("delete", "d", "🗑️"),
    "deletecollection": VerbDef("deletecollection", "dc", "🔥"),
    "watch": VerbDef("watch", "w", "👀"),
    "patch": VerbDef("patch", "p", "🩹"),
}
