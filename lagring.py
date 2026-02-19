from dataclasses import dataclass, field
from typing import TextIO

@dataclass
class CSVFil:
    navn: str
    kolonner: list[str]
    csv_fil: TextIO  = field(init=False)

    def __post_init__(self):
        self.csv_fil = open(self.navn, "a+")
        self._sjekk_header()

    def _sjekk_header(self):
        self.csv_fil.seek(0)
        rad  = self.csv_fil.readline()

        if rad == "":

            print("Tom",rad)
            self.csv_fil.write(f"{",".join(self.kolonner)}\n")
        else:
            print("Jerry", rad)
            self.csv_fil.seek(0,2)

    def lukk(self):
        self.csv_fil.close()


    def skriv(self, rad: list[str]):
        self.csv_fil.write(f"{",".join(rad)}\n")

    def les_hele_filen(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.csv_fil.close()
