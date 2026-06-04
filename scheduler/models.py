from dataclasses import dataclass
from typing import Optional


@dataclass
class Surgeon:
    name: str
    specialty: str
    off_day: str


@dataclass
class OperatingRoom:
    name: str
    room_type: str


@dataclass
class AnesthesiaTeam:
    name: str


@dataclass
class SurgeryRequest:
    patient: str
    operation: str
    duration: int
    priority: str
    required_specialty: str
    required_room: Optional[str] = None


@dataclass
class ScheduleItem:
    patient: str
    operation: str
    start_slot: int
    end_slot: int
    room: str
    surgeon: str
    anesthesia_team: str
