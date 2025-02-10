from dataclasses import dataclass


@dataclass
class VerbDef:
    name: str
    short: str
    emoji: str


all_verbs = {
    "get": VerbDef("get", "G", "🔍"),
    "list": VerbDef("list", "L", "📃"),
    "update": VerbDef("update", "U", "✍️"),
    "create": VerbDef("create", "C", "🌱"),
    "delete": VerbDef("delete", "D", "🗑️"),
    "deletecollection": VerbDef("deletecollection", "Dc", "🔥"),
    "watch": VerbDef("watch", "W", "👀"),
    "patch": VerbDef("patch", "P", "🩹"),
}
