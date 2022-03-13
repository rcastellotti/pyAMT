import xml.etree.ElementTree as ET
import requests
import csv
from datetime import datetime
import xmltodict
import re


class Line:
    def __init__(
        self,
        tipo,
        periodo,
        tipoGiorno,
        codiceLinea,
        barrato,
        targa,
        descrizione,
        firstLastString,
        firstStopAscDepartures,
        firstStopDiscDepartures,
    ):
        self.tipo = tipo
        self.periodo = periodo
        self.tipoGiorno = tipoGiorno
        self.codiceLinea = codiceLinea
        self.barrato = barrato
        self.targa = targa
        self.descrizione = descrizione
        self.firstStopAscLocation, self.lastStopAscLocation = re.split(
            r"\s-+>\s", firstLastString
        )
        self.firstStopAscDepartures = firstStopAscDepartures.split()
        self.firstStopDiscDepartures = firstStopDiscDepartures.split()

    def __repr__(self):
        return str(self.__dict__)


class Arrival:
    def __init__(
        self, lineName, destination, expectedArrivalTime, socialNumber, waitTime
    ):
        self.lineName = lineName
        self.destination = destination
        self.expectedArrivalTime = expectedArrivalTime
        self.socialNumber = socialNumber
        self.waitTime = waitTime

    def __repr__(self):
        return str(self.__dict__)

class Stop:
    def __init__(
        self, lineName, destination, expectedArrivalTime, socialNumber, waitTime
    ):
        self.lineName = lineName
        self.destination = destination
        self.expectedArrivalTime = expectedArrivalTime
        self.socialNumber = socialNumber
        self.waitTime = waitTime

    def __repr__(self):
        return str(self.__dict__)


class AMT:
    PASSAGGI_URL = "https://www.amt.genova.it/amt/servizi/passaggi_xml.php"
    STOPS_URL = "https://www.amt.genova.it/amt/servizi/app/dati/app_stops.php"
    LINES_URL = "https://www.amt.genova.it/amt/servizi/app/dati/app_lines.php"
    LINES_STOPS_URL = (
        "https://www.amt.genova.it/amt/servizi/app/dati/app_lines_stops.php"
    )
    LINE_URL = "https://www.amt.genova.it/amt/servizi/orari_xml.php"

    class LineNotFound(Exception):
        pass

    class StopNotFound(Exception):
        pass

    class LineStopsNotFound(Exception):
        pass

    def __init__(self):
        self._lines = requests.get(self.LINES_URL)
        self._lineStops = requests.get(self.LINES_STOPS_URL)

        pass

    def departures(self, codiceFermata: str):
        LINEA = 0
        DESTINAZIONE = 1
        TEORICA = 2
        PREVISIONE_PARTENZA = 3
        ORA_ARRIVO = 4
        PREVISIONE_ARRIVO = 5
        NUMERO_SOCIALE = 6
        CONTEGGIO_PASSEGGERI = 7
        AUTOBUS_PIENO = 8

        arrivals = []

        r = requests.get(self.PASSAGGI_URL, params={"CodiceFermata": codiceFermata})
        tree = ET.fromstring(r.content)
        for child in tree:
            arrival = Arrival(
                child[LINEA].text,
                child[DESTINAZIONE].text,
                child[ORA_ARRIVO].text,
                child[PREVISIONE_ARRIVO].text,
                child[NUMERO_SOCIALE].text,
            )
            arrivals.append(arrival)
        return arrivals

    def stop(self, ID: str):
        """get information about a stop"""

        stops = requests.get(self.STOPS_URL)
        text = f"ID;Name;Description;Lat;Lon;Lines;Monitored\n{stops.content.decode('utf-8')}"
        cr = csv.DictReader(text.splitlines(), delimiter=";")
        stop = list(filter(lambda p: p["ID"] == ID, cr))
        if stop:
            return stop[0]
        raise self.StopNotFound

    def line(self, ID: str):
        """get information about a line"""

        text = f"ID;Name;Start;End;Category;Description\n{self._lines.content.decode('utf-8')}"
        cr = csv.DictReader(text.splitlines(), delimiter=";")
        line = list(filter(lambda p: p["Name"] == ID, cr))
        if line:
            return line[0]
        raise self.LineNotFound

    def lineStops(self, ID: str):
        """get information about all lines and their stops"""

        text = f"VariantID;StopID;Position\n{self._lineStops.content.decode('utf-8')}"
        cr = csv.DictReader(text.splitlines(), delimiter=";")
        stops = list(filter(lambda p: p["VariantID"] == ID, cr))
        if stops:
            return stops
        raise self.LineStopsNotFound

    def linesDetailedInfo(
        self,
        lineName:str,
        gg=datetime.today().strftime("%d"),
        mm=datetime.today().strftime("%m"),
        aa=datetime.today().strftime("%Y"),
    ) -> list[Line]:
    
        """get detailed information about a line (including timetables)

        Arguments:
            lineName: name of bus line
            gg: day
            mm: month
            aa: year (for some reason this must be in YYYY format)
        Returns:
            bus lines matching the name
        Raises:
            LineNotFound: if line is not found
        """

        r = requests.get(
            self.LINE_URL, params={"linea": lineName, "gg": gg, "mm": mm, "aa": aa}
        )
        servizio = xmltodict.parse(r.content)["data"]["servizio"]
        lines = []
        for line in servizio["linea"]:
            # for some reason there's some junk, if a Line has no items we simply skip it
            if line["trattaasc"]["descrizione"]:
                currentLine = Line(
                    tipo=servizio["tipo"],
                    periodo=servizio["periodo"],
                    tipoGiorno=servizio["tipogiorno"],
                    codiceLinea=line["codice"],
                    barrato=line["barrato"],
                    targa=line["targa"],
                    descrizione=line["descrizione"],
                    firstStopAscDepartures=line["trattaasc"]["partenze"],
                    firstStopDiscDepartures=line["trattadisc"]["partenze"],
                    firstLastString=line["trattaasc"]["descrizione"],
                )
                lines.append(currentLine)
        if lines:
            return lines
        raise self.LineNotFound
