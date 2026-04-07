import os
from dataclasses import dataclass, field

DATA_DIR = os.environ.get("DATA_DIR", ".")

@dataclass
class CSVFil:
    navn: str
    kolonner: list[str]
    _sti: str = field(init=False, repr=False)

    def __post_init__(self):
        self._sti = os.path.join(DATA_DIR, self.navn)
        self._sjekk_header()

    def _sjekk_header(self):
        with open(self._sti, "a+") as fil:
            fil.seek(0)
            rad = fil.readline()
            if rad == "":
                fil.write(f"{",".join(self.kolonner)}\n")

    def skriv(self, rad: list[str]):
        with open(self._sti, "a") as f:
            f.write(f"{",".join(rad)}\n")

    def les_hele_filen(self):
        with open(self._sti, "r") as f:
            return f.readlines()
