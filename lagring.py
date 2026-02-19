from dataclasses import dataclass

@dataclass
class CSVFil:
    navn: str
    kolonner: list[str]

    def __post_init__(self):
        self._sjekk_header()

    def _sjekk_header(self):
        with open(self.navn, "a+") as fil:
            fil.seek(0)
            rad = fil.readline()
            if rad == "":
                fil.write(f"{",".join(self.kolonner)}\n")

    def skriv(self, rad: list[str]):
        with open(self.navn, "a") as f:
            f.write(f"{",".join(rad)}\n")

    def les_hele_filen(self):
        with open(self.navn, "r") as f:
            return f.readlines()
