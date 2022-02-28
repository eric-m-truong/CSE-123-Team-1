from dataclasses import dataclass, field

"""
id: Is assigned automatically by the database.
    We don't want to initialize it ourselves.
name:   Just the name of the plug (i.e. "Lamp").
        Assigned by the customer.

Intialization:
    new_plug = Plug("plug_name")
"""
@dataclass
class Plug:
    id: int = field(init=False)
    # hub_id: int
    name: float = ""

# @dataclass
# class Datapoint:
