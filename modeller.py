from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Runde:
    user_id: str
    runde_nummer: int
    start_tid: datetime
    slutt_tid: datetime = field(init=False)
    tid_brukt_minutter: int = field(init=False)
    tid_brukt_sekunder: int = field(init=False)

    def beregn(self):
        self.slutt_tid = datetime.now()
        delta_tid = self.slutt_tid - self.start_tid
        self.tid_brukt_minutter = delta_tid.seconds // 60
        self.tid_brukt_sekunder = delta_tid.seconds % 60


@dataclass
class Deltaker:
    id: str
    navn: str

    def rad(self):
        return [value for value in self.__dict__.values()]

