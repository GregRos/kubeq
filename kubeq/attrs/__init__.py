from .label import attr_Label
from .field import attr_Field
from .kind import attr_Kind

type attr_Api = attr_Label | attr_Field

type attr_Any = attr_Label | attr_Field | attr_Kind
