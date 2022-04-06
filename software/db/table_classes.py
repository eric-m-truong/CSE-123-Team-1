from dataclasses import dataclass, field
from datetime import datetime


"""
mac_addr:   The MAC Address of the plug.
is_on:      Whether the plug is on or off.
alias:      A more readable name for the plug (i.e. "Lamp").
            Assigned by the customer.

Intialization:
    new_plug = Plug(<fields>, ...)
"""
@dataclass
class Plug:
    mac_addr: str
    is_on: bool
    alias: str = ""


"""
timestamp:  Timestamp
plug_id:    Should match an existing Plug.id
power:      Power in kWh
"""
@dataclass
class Datapoint:
    timestamp: datetime
    plug_id: str
    power: float
