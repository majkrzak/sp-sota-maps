from dataclasses import dataclass
from typing import Self
from shapely import Polygon, Point
from owslib.wfs import WebFeatureService
from shapely.ops import transform
import geopandas as gpd
from geopandas import GeoDataFrame
from pandas import DataFrame, concat
from .bbox import Bbox
from .helpers.transformer import transformer


__all__ = ["Park"]


MAPPING = DataFrame(
    columns=["kodinspire", "FullName", "POTA", "WWFF"],
    data=[
        # fmt: off
        # National Parks
        ["PL.ZIPOP.1393.PN.5", "Pieniński Park Narodowy", "PL-0850", "SPFF-0013"],
        ["PL.ZIPOP.1393.PN.6", "Świętokrzyski Park Narodowy", "PL-0671", "SPFF-0018"],
        ["PL.ZIPOP.1393.PN.7", "Bieszczadzki Park Narodowy", "PL-0191", "SPFF-0004"],
        ["PL.ZIPOP.1393.PN.11", "Karkonoski Park Narodowy", "PL-1807", "SPFF-0009"],
        ["PL.ZIPOP.1393.PN.14", "Tatrzański Park Narodowy", "PL-0910", "SPFF-0019"],
        ["PL.ZIPOP.1393.PN.15", "Park Narodowy Gór Stołowych", "PL-1711", "SPFF-0017"],
        ["PL.ZIPOP.1393.PN.16", "Magurski Park Narodowy", "PL-0495", "SPFF-0010"],
        ["PL.ZIPOP.1393.PN.19", "Babiogórski Park Narodowy", "PL-1110", "SPFF-0001"],
        ["PL.ZIPOP.1393.PN.21", "Gorczański Park Narodowy", "PL-0881", "SPFF-0007"],
        # Landscape parks
        ["PL.ZIPOP.1393.PK.1", "Park Krajobrazowy Gór Sowich", "PL-1692", "SPFF-0087"],
        ["PL.ZIPOP.1393.PK.5", "Łagowsko-Sulęciński Park Krajobrazowy", "PL-1832", "SPFF-2687"],
        ["PL.ZIPOP.1393.PK.6", "Park Krajobrazowy Orlich Gniazd", "PL-1156", "SPFF-0093"],
        ["PL.ZIPOP.1393.PK.10", "Kaszubski Park Krajobrazowy", "PL-1476", "SPFF-0048"],
        ["PL.ZIPOP.1393.PK.11", "Park Krajobrazowy Góry Opawskie", "PL-1586", "SPFF-0085"],
        ["PL.ZIPOP.1393.PK.14", "Park Krajobrazowy Doliny Sanu", "PL-0239", "SPFF-0084"],
        ["PL.ZIPOP.1393.PK.15", "Park Krajobrazowy Gór Słonnych", "PL-0279", "SPFF-0086"],
        ["PL.ZIPOP.1393.PK.16", "Jaśliski Park Krajobrazowy", "PL-0442", "SPFF-0046"],
        ["PL.ZIPOP.1393.PK.18", "Park Krajobrazowy Beskidu Śląskiego", "PL-1320", "SPFF-0070"],
        ["PL.ZIPOP.1393.PK.26", "Park Krajobrazowy Beskidu Małego", "PL-1196", "SPFF-0069"],
        ["PL.ZIPOP.1393.PK.40", "Żywiecki Park Krajobrazowy", "PL-1234", "SPFF-0145"],
        ["PL.ZIPOP.1393.PK.47", "Park Krajobrazowy Góra Św. Anny", "PL-1474", "SPFF-0088"],
        ["PL.ZIPOP.1393.PK.55", "Park Krajobrazowy Wzgórz Dylewskich", "PL-0963", "SPFF-0106"],
        ["PL.ZIPOP.1393.PK.57", "Czarnorzecko-Strzyżowski Park Krajobrazowy", "PL-0402", "SPFF-0039"],
        ["PL.ZIPOP.1393.PK.90", "Popradzki Park Krajobrazowy", "PL-0788", "SPFF-0110"],
        ["PL.ZIPOP.1393.PK.98", "Ciśniańsko-Wetliński Park Krajobrazowy", "PL-0247", "SPFF-0038"],
        ["PL.ZIPOP.1393.PK.101", "Park Krajobrazowy Pasma Brzanki", "PL-0596", "SPFF-0094"],
        ["PL.ZIPOP.1393.PK.106", "Śnieżnicki Park Krajobrazowy", "PL-1635", "SPFF-0133"],
        ["PL.ZIPOP.1393.PK.114", "Jeleniowski Park Krajobrazowy", "PL-0598", "SPFF-1145"],
        ["PL.ZIPOP.1393.PK.143", "Rudawski Park Krajobrazowy", "PL-1782", "SPFF-0117"],
        ["PL.ZIPOP.1393.PK.144", "Park Krajobrazowy Sudetów Wałbrzyskich", "PL-1726", "SPFF-0104"],
        ["PL.ZIPOP.1393.PK.150", "Ślężański Park Krajobrazowy", "PL-1666", "SPFF-0132"],
        # Protected landscapes areas
        ["PL.ZIPOP.1393.OCHK.184", "Wschodniobeskidzki Obszar Chronionego Krajobrazu", "PL-0264", "SPFF-0910"],
        ["PL.ZIPOP.1393.OCHK.185", "Obszar Chronionego Krajobrazu Beskidu Niskiego", "PL-0471", "SPFF-0911"],
        ["PL.ZIPOP.1393.OCHK.186", "Hyżnieńsko-Gwoźnicki Obszar Chronionego Krajobrazu", "PL-0338", "SPFF-0820"],
        ["PL.ZIPOP.1393.OCHK.272", "Obszar Chronionego Krajobrazu Doliny Widawki", "PL-1125", "SPFF-1250"],
        ["PL.ZIPOP.1393.OCHK.279", "Południowomałopolski Obszar Chronionego Krajobrazu", "PL-0724", "SPFF-0384"],
        ["PL.ZIPOP.1393.OCHK.288", "Obszar Chronionego Krajobrazu Kopuły Chełmca", "PL-1731", "SPFF-1563"],
        ["PL.ZIPOP.1393.OCHK.291", "Obszar Chronionego Krajobrazu Ostrzyca Proboszczowicka", "PL-1791", "SPFF-1831"],
        ["PL.ZIPOP.1393.OCHK.345", "Obszar Chronionego Krajobrazu Góry Bardzkie i Sowie", "PL-1675", "SPFF-0414"],
        ["PL.ZIPOP.1393.OCHK.348", "Obszar Chronionego Krajobrazu Pogórza Ciężkowickiego", "PL-0631", "SPFF-0970"],
        ["PL.ZIPOP.1393.OCHK.364", "Obszar Chronionego Krajobrazu Masyw Trójgarbu", "PL-2593", "SPFF-2410"],
        ["PL.ZIPOP.1393.OCHK.365", "Obszar Chronionego Krajobrazu Góry Bystrzyckie i Orlickie", "PL-1695", "SPFF-1006"],
        ["PL.ZIPOP.1393.OCHK.502", "Obszar Chronionego Krajobrazu Pogórza Ciężkowickiego", "PL-0631", "SPFF-0970"],
        ["PL.ZIPOP.1393.OCHK.625", "Obszar Chronionego Krajobrazu Wzgórz Szeskich", "PL-0256", "SPFF-1351"],
        # Rezerwaty
        ["PL.ZIPOP.1393.RP.137", "Rezerwat przyrody Kostrza", "PL-2198", "SPFF-2233"],
        ["PL.ZIPOP.1393.RP.188", "Rezerwat przyrody Szczyt Wieżyca na Pojezierzu Kaszubskim", "PL-1492", "SPFF-0644"],
        ["PL.ZIPOP.1393.RP.196", "Rezerwat przyrody Romanka", "PL-2160", "SPFF-2247"],
        ["PL.ZIPOP.1393.RP.203", "Rezerwat przyrody Rezerwat Tysiąclecia na Cergowej Górze", "PL-0425", "SPFF-1056"],
        ["PL.ZIPOP.1393.RP.605", "Rezerwat przyrody Barania Góra", "PL-0806", "SPFF-0756"],
        ["PL.ZIPOP.1393.RP.664", "Rezerwat przyrody Czantoria", "PL-1976", "SPFF-2223"],
        ["PL.ZIPOP.1393.RP.703", "Rezerwat przyrody Na Policy", "PL-2662", ""],
        ["PL.ZIPOP.1393.RP.777", "Rezerwat przyrody Wilcze", "PL-0353", "SPFF-0829"],
        ["PL.ZIPOP.1393.RP.919", "Rezerwat przyrody Mogielica", "PL-2291", "SPFF-2425"],
        ["PL.ZIPOP.1393.RP.930", "Rezerwat przyrody Madohora", "PL-2184", "SPFF-2236"],
        ["PL.ZIPOP.1393.RP.963", "Rezerwat przyrody Kamień nad Jaśliskami", "PL-2158", "SPFF-2325"],
        ["PL.ZIPOP.1393.RP.987", "Rezerwat przyrody Luboń Wielki", "PL-0949", "SPFF-0223"],
        ["PL.ZIPOP.1393.RP.1002", "Rezerwat przyrody Rezerwat na Policy im.prof.Zenona Klemensiewicza", "PL-1075", "SPFF-0147"],
        ["PL.ZIPOP.1393.RP.1004", "Rezerwat przyrody Wierchomla,PL-0698", "SPFF-0445"],
        ["PL.ZIPOP.1393.RP.1010", "Rezerwat przyrody Wysokie Skałki", "PL-0787", "SPFF-1245"],
        ["PL.ZIPOP.1393.RP.1017", "Rezerwat przyrody Szczytniak", "PL-0593", "SPFF-0159"],
        ["PL.ZIPOP.1393.RP.1063", "Rezerwat przyrody Oszast", "PL-1977", "SPFF-2244"],
        ["PL.ZIPOP.1393.RP.1068", "Rezerwat przyrody Lipowska", "PL-1975", "SPFF-2234"],
        ["PL.ZIPOP.1393.RP.1076", "Rezerwat przyrody Góra Ślęża", "PL-1669", "SPFF-0930"],
        ["PL.ZIPOP.1393.RP.1107", "Rezerwat przyrody Chwaniów", "PL-0216", "SPFF-1064"],
        ["PL.ZIPOP.1393.RP.1114", "Rezerwat przyrody Góra Radunia", "PL-1662", "SPFF-1009"],
        ["PL.ZIPOP.1393.RP.1133", "Rezerwat przyrody Śnieżnik Kłodzki", "PL-1640", "SPFF-1364"],
        ["PL.ZIPOP.1393.RP.1151", "Rezerwat przyrody Ostrzyca Proboszczowicka", "PL-1792", "SPFF-1831"],
        ["PL.ZIPOP.1393.RP.1229", "Rezerwat przyrody Baniska", "PL-2741", ""],
        ["PL.ZIPOP.1393.RP.1338", "Rezerwat przyrody Bukowa Kalenica w Górach Sowich", "PL-1690", "SPFF-0722"],
        ["PL.ZIPOP.1393.RP.1386", "Rezerwat przyrody Źródliska Jasiołki", "PL-2140", "SPFF-2358"],
        ["PL.ZIPOP.1393.RP.1608", "Rezerwat przyrody Przysłup", "", ""],
        # Natura 2000
        # Combined areas
        ["PL.ZIPOP.1393.N2K.PLC020001.B", "Obszar (ptasi) Natura 2000 Karkonosze", "PL-1804", "SPFF-0403"], # referenced separatley
        ["PL.ZIPOP.1393.N2K.PLC020001.H", "Obszar (siedliskowy) Natura 2000 Karkonosze", "PL-1806", "SPFF-0404"], # referenced separatley
        ["PL.ZIPOP.1393.N2K.PLC120001.B", "Obszar (ptasi) Natura 2000 Tatry", "PL-2597", ""], # referenced separatley
        ["PL.ZIPOP.1393.N2K.PLC120001.H", "Obszar (siedliskowy) Natura 2000 Tatry", "PL-2599", ""], # referenced separatley
        ["PL.ZIPOP.1393.N2K.PLC120002.B", "Obszar Natura 2000 Pieniny", "", ""],  # not explicitly referenced
        ["PL.ZIPOP.1393.N2K.PLC120002.H", "Obszar Natura 2000 Pieniny", "PL-0838", "SPFF-0388"],
        ["PL.ZIPOP.1393.N2K.PLC180001.B", "Obszar Natura 2000 Bieszczady", "PL-0227", "SPFF-0435"],  # referenced once
        ["PL.ZIPOP.1393.N2K.PLC180001.H", "Obszar Natura 2000 Bieszczady", "PL-0227", "SPFF-0435"],  # referenced once
        # Not combined areass
        ["PL.ZIPOP.1393.N2K.PLB020006.B", "Obszar (ptasi) Natura 2000 Góry Stołowe", "PL-2340", "SPFF-2447"],
        ["PL.ZIPOP.1393.N2K.PLH020004.H", "Obszar (siedliskowy) Natura 2000 Góry Stołowe", "PL-2560", ""],
        ["PL.ZIPOP.1393.N2K.PLB120001.B", "Obszar Natura 2000 Gorce", "PL-2486", "SPFF-2516"],
        ["PL.ZIPOP.1393.N2K.PLH120018.H", "Obszar Natura 2000 Ostoja Gorczańska", "PL-0921", "SPFF-1692"],
        ["PL.ZIPOP.1393.N2K.PLB120011.B", "Obszar Natura 2000 Babia Góra", "PL-2714", ""],
        ["PL.ZIPOP.1393.N2K.PLH120001.H", "Obszar Natura 2000 Ostoja Babiogórska", "PL-2715", ""],
        ["PL.ZIPOP.1393.N2K.PLB180003.B", "Obszar Natura 2000 Góry Słonne", "", ""],
        ["PL.ZIPOP.1393.N2K.PLH180013.H", "Obszar Natura 2000 Ostoja Góry Słonne", "", ""],
        ["PL.ZIPOP.1393.N2K.PLB240002.B", "Obszar Natura 2000 Beskid Żywiecki", "PL-2016", "SPFF-2166"], # referenced once
        ["PL.ZIPOP.1393.N2K.PLH240006.H", "Obszar Natura 2000 Beskid Żywiecki", "PL-2016", "SPFF-2166"], # referenced once
        # Unique areas
        ["PL.ZIPOP.1393.N2K.PLB020009.B", "Obszar Natura 2000 Góry Izerskie", "PL-2095", "SPFF-2147"],
        ["PL.ZIPOP.1393.N2K.PLB020010.B", "Obszar Natura 2000 Sudety Wałbrzysko-Kamiennogórskie", "PL-1751", "SPFF-1846"],
        ["PL.ZIPOP.1393.N2K.PLB120006.B", "Obszar Natura 2000 Pasmo Policy", "PL-2663", "SPFF-2738"],
        ["PL.ZIPOP.1393.N2K.PLB180002.B", "Obszar Natura 2000 Beskid Niski", "PL-0426", "SPFF-1837"],
        ["PL.ZIPOP.1393.N2K.PLH020016.H", "Obszar Natura 2000 Góry Bialskie i Grupa Śnieżnika", "PL-2407", "SPFF-2518"],
        ["PL.ZIPOP.1393.N2K.PLH020021.H", "Obszar Natura 2000 Wzgórza Kiełczyńskie", "", "SPFF-2676"],
        ["PL.ZIPOP.1393.N2K.PLH020037.H", "Obszar Natura 2000 Góry i Pogórze Kaczawskie", "PL-1773", "SPFF-0272"],
        ["PL.ZIPOP.1393.N2K.PLH020038.H", "Obszar Natura 2000 Góry Kamienne", "PL-1738", "SPFF-1832"],
        ["PL.ZIPOP.1393.N2K.PLH020040.H", "Obszar Natura 2000 Masyw Ślęży", "PL-2665", ""],
        ["PL.ZIPOP.1393.N2K.PLH020042.H", "Obszar Natura 2000 Ostrzyca Proboszczowicka", "", ""],
        ["PL.ZIPOP.1393.N2K.PLH020047.H", "Obszar Natura 2000 Torfowiska Gór Izerskich", "PL-1828", "SPFF-0438"],
        ["PL.ZIPOP.1393.N2K.PLH020057.H", "Obszar Natura 2000 Masyw Chełmca", "PL-2297", "SPFF-2384"],
        ["PL.ZIPOP.1393.N2K.PLH020071.H", "Obszar Natura 2000 Ostoja Nietoperzy Gór Sowich", "PL-1694", "SPFF-2534"],
        ["PL.ZIPOP.1393.N2K.PLH020096.H", "Obszar Natura 2000 Góry Złote", "PL-2683", ""],
        ["PL.ZIPOP.1393.N2K.PLH080008.H", "Obszar Natura 2000 Buczyny Łagowsko-Sulęcińskie", "PL-2711", "SPFF-2687"],
        ["PL.ZIPOP.1393.N2K.PLH120012.H", "Obszar Natura 2000 Na Policy", "PL-2664", ""],
        ["PL.ZIPOP.1393.N2K.PLH120019.H", "Obszar Natura 2000 Ostoja Popradzka", "PL-2400", "SPFF-2457"],
        ["PL.ZIPOP.1393.N2K.PLH120025.H", "Obszar Natura 2000 Małe Pieniny", "PL-2516", "SPFF-2530"],
        ["PL.ZIPOP.1393.N2K.PLH120036.H", "Obszar Natura 2000 Łabowa", "", "SPFF-2626"],
        ["PL.ZIPOP.1393.N2K.PLH120043.H", "Obszar Natura 2000 Luboń Wielki", "PL-0949", ""],
        ["PL.ZIPOP.1393.N2K.PLH120047.H", "Obszar Natura 2000 Ostoja w Paśmie Brzanki", "PL-2607", ""],
        ["PL.ZIPOP.1393.N2K.PLH120052.H", "Obszar Natura 2000 Ostoje Nietoperzy Beskidu Wyspowego", "PL-2224", "SPFF-2534"],
        ["PL.ZIPOP.1393.N2K.PLH120081.H", "Obszar Natura 2000 Lubogoszcz", "PL-2260", "SPFF-2382"],
        ["PL.ZIPOP.1393.N2K.PLH120094.H", "Obszar Natura 2000 Ostoje Nietoperzy Powiatu Gorlickiego", "PL-0609", "SPFF-1594"],
        ["PL.ZIPOP.1393.N2K.PLH160002.H", "Obszar Natura 2000 Góra Świętej Anny", "PL-1462", "SPFF-0246"],
        ["PL.ZIPOP.1393.N2K.PLH160007.H", "Obszar Natura 2000 Góry Opawskie", "PL-1559", "SPFF-1611"],
        ["PL.ZIPOP.1393.N2K.PLH180001.H", "Obszar Natura 2000 Ostoja Magurska", "PL-1993", "SPFF-2125"],
        ["PL.ZIPOP.1393.N2K.PLH180014.H", "Obszar Natura 2000 Ostoja Jaśliska", "PL-2513", "SPFF-2456"],
        ["PL.ZIPOP.1393.N2K.PLH180015.H", "Obszar Natura 2000 Łysa Góra", "PL-0463", "SPFF-1902"],
        ["PL.ZIPOP.1393.N2K.PLH180018.H", "Obszar Natura 2000 Trzciana", "PL-0438", "SPFF-1896"],
        ["PL.ZIPOP.1393.N2K.PLH180027.H", "Obszar Natura 2000 Ostoja Czarnorzecka", "PL-0392", "SPFF-1719"],
        ["PL.ZIPOP.1393.N2K.PLH180046.H", "Obszar Natura 2000 Liwocz", "PL-2007", "SPFF-2133"],
        ["PL.ZIPOP.1393.N2K.PLH220095.H", "Obszar Natura 2000 Uroczyska Pojezierza Kaszubskiego", "PL-2485", "SPFF-2397"],
        ["PL.ZIPOP.1393.N2K.PLH240005.H", "Obszar Natura 2000 Beskid Śląski", "PL-2118", "SPFF-2165"],
        ["PL.ZIPOP.1393.N2K.PLH240023.H", "Obszar Natura 2000 Beskid Mały", "PL-2054", "SPFF-2164"],
        ["PL.ZIPOP.1393.N2K.PLH260002.H", "Obszar Natura 2000 Łysogóry", "PL-0663", "SPFF-0549"],
        ["PL.ZIPOP.1393.N2K.PLH260028.H", "Obszar Natura 2000 Ostoja Jeleniowska", "PL-0584", "SPFF-1640"],
        ["PL.ZIPOP.1393.N2K.PLH280043.H", "Obszar Natura 2000 Ostoja Dylewskie Wzgórza", "PL-2423", "SPFF-2455"],
        # Others
        ["PL.ZIPOP.1393.PP.1801052.31", "", "", ""],
        ["PL.ZIPOP.1393.PP.1215072.2053", "", "", ""],
        ["PL.ZIPOP.1393.PP.1205102.3160", "", "", ""],
        ["PL.ZIPOP.1393.UE.1821022.372", "", "", ""],
        ["PL.ZIPOP.1393.ZPK.41", "Zespół przyrodniczo-krajobrazowy Kokocz", "", "SPFF-2717"],
        ["PL.ZIPOP.1393.ZPK.334", "Zespół przyrodniczo-krajobrazowy Dolina Wapienicy", "PL-1278", "SPFF-0474"],
        ["PL.ZIPOP.1393.ZPK.347", "Zespół przyrodniczo-krajobrazowy Dolina Skawicy", "PL-2394", "SPFF-2058"],
        # fmt: on
    ],
).set_index("kodinspire")


TYPES = [
    "GDOS:ParkiNarodowe",
    "GDOS:ParkiKrajobrazowe",
    "GDOS:Rezerwaty",
    "GDOS:ObszaryChronionegoKrajobrazu",
    "GDOS:ZespolyPrzyrodniczoKrajobrazowe",
    "GDOS:ObszarySpecjalnejOchrony",
    "GDOS:SpecjalneObszaryOchrony",
    "GDOS:PomnikiPrzyrodyPowierzchniowe",
    "GDOS:UzytkiEkologiczne",
]

WFS = WebFeatureService(
    url="https://sdi.gdos.gov.pl/wfs",
    version="1.1.0",
    # auth=Authentication(None, None, None, False),
)


def read_wfs(bbox):
    response = WFS.getfeature(
        typename=TYPES,
        bbox=bbox.t(2180).xyxy,
    )

    data = []
    for typ in TYPES:
        try:
            data.append(gpd.read_file(response, layer=typ[5:]))
        except:
            pass

    if not len(data):
        return GeoDataFrame(
            {"nazwa": ["otulina"], "kodinspire": ["abs"], "geometry": [Point(0, 0)]}
        )
    else:
        return concat(data)


@dataclass
class Park:
    name: str
    pota: str
    wwff: str

    @classmethod
    def find(self, shape: Polygon) -> list[Self]:

        data = read_wfs(Bbox.new(shape, 100))

        data.nazwa = data.nazwa.astype("str")
        data = data[~data.nazwa.str.endswith("otulina")]

        data = data[
            data.apply(
                lambda x: not transform(
                    transformer(4326, 2180).transform, shape
                ).disjoint(x.geometry),
                axis=1,
            )
        ]
        data = data.set_index("kodinspire", drop=False)
        data = data.join(MAPPING, validate="one_to_one")

        assert data.FullName.notna().all()

        data = data.groupby(["FullName", "POTA", "WWFF"], sort=False).agg(
            {
                "FullName": "first",
                "POTA": "first",
                "WWFF": "first",
            }
        )
        return [
            Park(row["FullName"], row["POTA"], row["WWFF"])
            for _, row in data.iterrows()
        ]
