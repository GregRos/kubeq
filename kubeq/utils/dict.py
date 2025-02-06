from typing import Hashable, Mapping


def keys_of_type[
    TSuperKey: Hashable, TKey: Hashable, TVal
](d: Mapping[TSuperKey, TVal], t: type[TKey]) -> Mapping[TKey, TVal]:
    return {k: v for k, v in d.items() if isinstance(k, t)}
