from dataclasses import dataclass
from typing import Self, ClassVar
from shapely import Polygon
from owslib.wfs import WebFeatureService
from shapely.ops import transform
import geopandas as gpd
from .bbox import Bbox
from .helpers.transformer import transformer

__all__ = ["Gmina"]

WFS = WebFeatureService(
    url="https://mapy.geoportal.gov.pl/wss/service/PZGIK/PRG/WFS/AdministrativeBoundaries",
    version="1.1.0",
)


def read_wfs(bbox):
    response = WFS.getfeature(
        typename=["A03_Granice_gmin"],
        bbox=bbox.t(2180).r().xyxy,
    )

    with open(f"data.xml", "wb") as f:
        f.write(response.read())

    try:
        return gpd.read_file("data.xml")
    except:
        return None


@dataclass
class Gmina:
    PGA: ClassVar[dict[str, str]] = {
        "1207112": "LI11",
        "1207112": "LI03",
        "1801052": "UD02",
        "1821022": "LK02",
        "1817042": "SA04",
        "1821012": "LK01",
        "1817073": "SA07",
        "1805022": "JS02",
        "1819022": "SY02",
        "1216103": "TA11",
        "1216063": "TA06",
        "1819032": "SY03",
        "1205102": "GO10",
        "1210082": "NS08",
        "1821052": "LK05",
        "1807052": "KS05",
        "1216162": "TA09",
        "0202062": "DZ06",
        "0223073": "WR07",
        "1012053": "RE05",
        "0807043": "SN04",
        "2205062": "RU06",
        "1815052": "RO05",
        "1817052": "SA05",
        "1216042": "TA04",
        "1803063": "DE06",
        "1816023": "RZ02",
        "1210042": "NS04",
        "1205092": "GO09",
        "0208103": "KV10",
        "0207042": "KQ04",
        "1217011": "ZP01",
        "1819052": "SY05",
        "1210052": "NS05",
        "1807102": "KS10",
        "1805032": "JS03",
        "1805062": "JS06",
        "1207052": "LI05",
        "1205082": "GO08",
        "1817032": "SA03",
        "1210073": "NS07",
        "1807083": "KS08",
        "1205042": "GO04",
        "0205023": "JR02",
        "0221063": "AB07",
        "0202052": "DZ05",
        "1209082": "MQ08",
        "1807023": "KS02",
        "1805072": "TR06",
        "1801032": "UD01",
        "2416063": "ZW06",
        "1611043": "TE04",
        "1217042": "ZP04",
        "0221021": "AB02",
        "1211102": "NT09",
        "1215063": "SB06",
        "1207092": "LI09",
        "1801083": "UD03",
        "1821033": "LK03",
        "1821042": "LK04",
        "2417112": "ZC11",
        "1209022": "MQ02",
        "1210092": "NS09",
        "1209092": "MQ09",
        "0206052": "JG05",
        "1817062": "SA06",
        "1211072": "NT06",
        "1211052": "NT04",
        "1211092": "NT08",
        "1211062": "NT05",
        "1201092": "BO09",
        "0207022": "KQ02",
        "1207072": "LI07",
        "1215082": "SB08",
        "2417152": "ZC15",
        "1217032": "ZP03",
        "0226043": "ZT04",
        "0206072": "JG07",
        "2604023": "KI02",
        "2403042": "CY04",
        "2417062": "ZC06",
        "1215042": "SB04",
        "2417042": "ZC04",
        "2417142": "ZC14",
        "1211023": "NT14",
        "2402011": "BB01",
        "1210152": "NS15",
        "2417092": "ZC09",
        "1211042": "NT03",
        "1207032": "LI03",
        "2461011": "BH01",
        "1210113": "NS11",
        "0226032": "ZT03",
        "0206062": "JG06",
        "0212043": "LF04",
        "0206041": "JG04",
        "0208083": "KV08",
        "1607013": "NF01",
        "0208063": "KV06",
        "0208133": "KV13",
        "0207033": "KQ03",
        "0208041": "KV04",
        "0208072": "KV07",
        "0221042": "AB05",
        "0221031": "AB03",
        "0208123": "KV13",
        "0221053": "AB06",
        "0208112": "KV11",
        "0219052": "ID05",
        "2813032": "OX01",
        "2815092": "OQ09",
        "1211042": "NT03",
        "0206031": "JG03",
        "2610032": "SQ03",
        "2607062": "OS06",
        "1207122": "LJ12",
        "2403021": "CY02",
        "1218052": "WA05",
        "2417011": "ZC01",
        "1215072": "SB07",
        "1207042": "LI04",
        "2417132": "ZC13",
        "2402082": "BB08",
        "1201082": "BO08",
        "2417092": "ZC09",
        "1207032": "LI03",
        "2402072": "BB07",
        "1215052": "SB05",
        "2403092": "CY09",
        "1215021": "SB02",
        "2403031": "CY03",
        "2402102": "BB10",
        "2417052": "ZC05",
        "1210133": "NS13",
        "1207082": "LI08",
        "1211123": "NT11",
        "1207021": "LI02",
        "1211112": "NT10",
        "1211033": "NT02",
        "2417082": "ZC08",
        "1218013": "WA01",
        "1207062": "LI06",
        "1209042": "MQ04",
        "2417072": "ZC07",
        "2417022": "ZC02",
        "2417122": "ZC12",
        "1218093": "WA09",
        "0202033": "DZ03",
        "0202011": "DZ01",
        "0265011": "WB01",
        "0221072": "AB08",
        "0224073": "ZS07",
        "0206011": "JG01",
        "2403072": "CY07",
        "1817042": "SA04",
    }

    id: str
    name: str

    @property
    def pga(self):
        return PGA[self.id]

    @classmethod
    def find(cls, shape: Polygon) -> list[Self]:

        data = read_wfs(Bbox.new(shape, 100))
        data = data[data["WAZNY_DO"].astype(str) == "0"]

        data = data[
            data.apply(
                lambda x: not transform(
                    transformer(4326, 2180).transform, shape
                ).disjoint(x.geometry),
                axis=1,
            )
        ]

        return [
            Gmina(row["JPT_KOD_JE"], row["JPT_NAZWA_"]) for _, row in data.iterrows()
        ]
