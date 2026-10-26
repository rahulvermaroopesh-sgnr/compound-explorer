import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pharma Compound Explorer", page_icon="💊", layout="wide")

# ---------------------------------------------------------------
# Skin: dark teal HUD (Qgen / BioPrism inspired)
# ---------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Rajdhani:wght@500;600;700&display=swap');
:root{--bg:#04100f;--panel:rgba(14,38,36,.62);--line:rgba(70,230,200,.22);--cyan:#35f0d0;--mint:#4be3a2;--violet:#8b6cff;--text:#d7ece8;--mut:#7fa39d;}
.stApp{background:radial-gradient(1200px 600px at 75% -10%,rgba(40,170,150,.28),transparent 60%),radial-gradient(900px 500px at -10% 30%,rgba(90,70,200,.16),transparent 60%),var(--bg);color:var(--text);font-family:'Barlow',sans-serif;}
.stApp p,.stApp li,.stApp label,.stApp span,.stApp td,.stApp th,.stApp div{color:var(--text);}
header[data-testid="stHeader"]{background:transparent;}
section[data-testid="stSidebar"]{background:rgba(6,22,21,.92);border-right:1px solid var(--line);}
h1,h2,h3{font-family:'Rajdhani',sans-serif!important;letter-spacing:.02em;}
.hero{padding:26px 28px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,rgba(20,60,56,.55),rgba(30,24,70,.45));box-shadow:0 0 40px rgba(53,240,208,.08) inset;margin-bottom:18px;}
.hero h1{margin:0;font-size:2.5rem;font-weight:700;background:linear-gradient(90deg,#9b86ff,#35f0d0);-webkit-background-clip:text;background-clip:text;color:transparent!important;}
.hero p{margin:6px 0 0;color:var(--mut);}
.nodes{display:flex;gap:18px;flex-wrap:wrap;margin-top:16px;}
.node{display:flex;align-items:center;gap:10px;}
.hex{width:34px;height:38px;clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);display:flex;align-items:center;justify-content:center;font:700 14px Rajdhani,sans-serif;color:#04100f!important;}
.hex.a{background:var(--cyan);}.hex.b{background:var(--violet);}.hex.c{background:var(--mint);}
.node span{font-size:.9rem;color:var(--text);}
.glass{border:1px solid var(--line);border-radius:14px;background:var(--panel);padding:16px 18px;}
.hud{border-left:2px solid var(--cyan);padding:6px 14px;background:linear-gradient(90deg,rgba(53,240,208,.10),transparent);border-radius:4px;margin-bottom:8px;}
.hud-l{font-size:.75rem;color:var(--mut);}
.hud-v{font:600 1.7rem Rajdhani,sans-serif;color:var(--cyan)!important;line-height:1.15;}
.hud-v.s{font-size:1.05rem;}
.pill{display:inline-block;padding:3px 12px;border:1px solid var(--line);border-radius:999px;font-size:.8rem;color:var(--mint)!important;margin:2px 6px 2px 0;}
.ids{font-size:.88rem;color:var(--mut);line-height:1.7;}
.ids code{color:var(--cyan)!important;background:rgba(53,240,208,.08);}
[data-testid="stImage"]{border:1px solid var(--line);border-radius:14px;padding:10px;background:rgba(6,24,23,.8);}
[data-testid="stImage"] img{filter:invert(.92) hue-rotate(180deg);border-radius:8px;}
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:999px 999px 0 0;padding:8px 16px;color:var(--mut);}
.stTabs [aria-selected="true"]{background:rgba(53,240,208,.12);color:var(--cyan)!important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--cyan);}
[data-testid="stTable"] table{background:transparent;border-collapse:collapse;width:100%;}
[data-testid="stTable"] th,[data-testid="stTable"] td{border:0!important;border-bottom:1px solid rgba(70,230,200,.12)!important;padding:9px 10px!important;background:transparent!important;}
[data-testid="stTable"] th{color:var(--mut)!important;font-weight:500;}
[data-testid="stAlert"]{background:rgba(255,120,80,.10);border:1px solid rgba(255,140,100,.35);border-radius:12px;}
.rx{padding:8px 0;border-bottom:1px solid rgba(70,230,200,.12);}
.rx b{color:var(--cyan)!important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------
# Compound database (typical literature values; educational use)
# ---------------------------------------------------------------
COMPOUNDS = {
    "Paracetamol": {
        "cid": 1983,
        "formula": "C8H9NO2",
        "mass": "151.16 g/mol",
        "class": "Analgesic / antipyretic",
        "ids": [("IUPAC name", "N-(4-Hydroxyphenyl)acetamide"), ("Also called", "Acetaminophen"),
                ("CAS", "103-90-2"), ("SMILES", "CC(=O)Nc1ccc(O)cc1")],
        "description": (
            "One of the most widely used over-the-counter medicines for pain and fever. "
            "A white crystalline solid with a phenolic -OH and an amide group on a "
            "para-substituted benzene ring. It has very little anti-inflammatory action."
        ),
        "physical": {
            "Molar mass (g/mol)": 151.16,
            "Appearance": "White crystalline powder",
            "Odour / taste": "Odourless, slightly bitter",
            "Melting point (°C)": 169,
            "Boiling point (°C)": "≈ 420 (decomposes)",
            "Density (g/mL)": 1.29,
            "Water solubility (g/L, ~20 °C)": 14,
            "LogP": 0.5,
        },
        "chemical": {
            "Functional groups": "Phenolic -OH, secondary amide, benzene ring (para)",
            "Acidity (pKa of -OH)": "≈ 9.5",
            "Hydrolysis": "Slowly gives 4-aminophenol + acetic acid (acid/base, heat)",
            "Mechanism": "Inhibits COX mainly in the CNS; exact mechanism still debated",
            "Half-life": "≈ 1-4 h (adults)",
            "Protein binding": "≈ 10-25 %",
            "Metabolism": "Liver: glucuronidation (~50-60 %), sulfation (~30 %), CYP2E1 → NAPQI (<10 %, detoxified by glutathione)",
            "Excretion": "Mainly urine as conjugates",
        },
        "reactions": [
            ("Ferric chloride test", "Violet-blue colour (phenolic -OH)."),
            ("Acid/base hydrolysis", "Amide cleaves to 4-aminophenol and acetic acid."),
            ("Bromine water", "Decolourised (activated aromatic ring)."),
            ("Textbook preparation", "Acetylation of 4-aminophenol with acetic anhydride."),
        ],
        "tests": [
            ("FeCl3", "Violet-blue colour"),
            ("Bromine water", "Decolourised / pale precipitate"),
            ("Melting point", "≈ 169-170 °C (purity check)"),
            ("UV (in water/methanol)", "λmax ≈ 245 nm"),
        ],
        "uses": ["Pain relief (headache, toothache, muscle pain)", "Fever reduction",
                 "Combination cold and flu products", "Safer than NSAIDs for stomach, but not anti-inflammatory"],
        "safety": ("Overdose can cause serious liver damage, sometimes without early symptoms. "
                   "Do not exceed the dose on the label (adult maximum is usually 4 g/day), avoid "
                   "taking several paracetamol-containing products together, and limit alcohol. "
                   "In overdose seek emergency care immediately; N-acetylcysteine is the antidote."),
        "cmp": {"Type": "Synthetic drug", "Primary use": "Pain and fever", "Mechanism": "COX inhibition (central)",
                "Legal status": "Over the counter (most countries)", "num": (151.16, 2.0, 20)},
    },
    "Levocetirizine": {
        "cid": 1549000,
        "formula": "C21H25ClN2O3",
        "mass": "388.89 g/mol",
        "class": "2nd-gen antihistamine",
        "ids": [("IUPAC name", "2-[2-[4-[(R)-(4-Chlorophenyl)(phenyl)methyl]piperazin-1-yl]ethoxy]acetic acid"),
                ("CAS", "130018-77-8"), ("SMILES (no stereo)", "OC(=O)COCCN1CCN(CC1)C(c1ccccc1)c1ccc(Cl)cc1")],
        "description": (
            "The active (R)-enantiomer of cetirizine. It blocks histamine H1 receptors and is used "
            "for allergic rhinitis and chronic hives. Being a second-generation antihistamine, it "
            "causes less drowsiness than older ones. Tablets usually contain the dihydrochloride salt."
        ),
        "physical": {
            "Molar mass (g/mol)": 388.89,
            "Molar mass, dihydrochloride (g/mol)": 461.81,
            "Appearance": "White to off-white crystalline powder (salt)",
            "Odour": "Odourless",
            "Melting point (°C)": None,
            "Boiling point (°C)": None,
            "Density (g/mL)": None,
            "Water solubility": "Very soluble (dihydrochloride salt)",
            "Log D (pH 7.4)": "≈ 1.5",
        },
        "chemical": {
            "Functional groups": "Carboxylic acid, ether, tertiary amines (piperazine), chlorophenyl, phenyl",
            "Chirality": "One stereocentre; (R)-form is the active enantiomer",
            "Ionisation": "Zwitterion at body pH (pKa ≈ 2.9 acid; ≈ 8 amine)",
            "Mechanism": "Selective H1-receptor inverse agonist",
            "Half-life": "≈ 8 h",
            "Protein binding": "≈ 91-92 %",
            "Bioavailability": "> 85 %, peak in about 1 h",
            "Metabolism / excretion": "Minimal metabolism; ≈ 85 % excreted unchanged in urine",
        },
        "reactions": [
            ("Salt formation", "Reacts with HCl to give the water-soluble dihydrochloride used in tablets."),
            ("Esterification", "The -COOH group can form esters with alcohols under acid catalysis."),
            ("Oxidative degradation", "Amine can oxidise to an N-oxide impurity under stress conditions."),
            ("Dragendorff's reagent", "Orange-red precipitate (tertiary amine / alkaloid-type test)."),
        ],
        "tests": [
            ("UV absorption", "λmax ≈ 230 nm"),
            ("HPLC-UV", "Standard assay method in pharmacopoeias"),
            ("Chiral HPLC", "Separates (R) from (S) enantiomer"),
            ("Dragendorff's", "Orange-red precipitate"),
        ],
        "uses": ["Allergic rhinitis (seasonal and perennial)", "Chronic idiopathic urticaria (hives)",
                 "Itching and sneezing from allergies", "Usual adult dose on labels is 5 mg once daily"],
        "safety": ("May cause drowsiness, dry mouth or tiredness; avoid alcohol and be careful when driving. "
                   "Dose needs adjusting in kidney impairment. Avoid in known hypersensitivity to cetirizine "
                   "or hydroxyzine. Availability (OTC or prescription) varies by country, so follow the "
                   "product label or your doctor."),
        "cmp": {"Type": "Synthetic drug", "Primary use": "Allergy relief", "Mechanism": "H1-receptor blockade",
                "Legal status": "OTC or prescription (varies by country)", "num": (388.89, 8.0, 91.5)},
    },
    "Opium poppy": {
        "cid": 5288826,
        "formula": "C17H19NO3 (morphine)",
        "mass": "285.34 g/mol (morphine)",
        "class": "Medicinal plant (alkaloid source)",
        "ids": [("Botanical name", "Papaver somniferum L. (family Papaveraceae)"),
                ("Structure shown", "Morphine, the principal alkaloid"), ("Morphine CAS", "57-27-2"),
                ("Morphine SMILES", "CN1CC[C@]23[C@@H]4[C@H]1CC5=C2C(=C(C=C5)O)O[C@H]3[C@H](C=C4)O")],
        "description": (
            "A flowering annual plant whose unripe seed capsule yields a milky latex (opium) rich in "
            "alkaloids. It is the natural source of morphine and codeine, and of papaverine and "
            "noscapine. The mature seeds are used in food and contain negligible alkaloids."
        ),
        "physical": {
            "Botanical name": "Papaver somniferum",
            "Family": "Papaveraceae",
            "Plant height": "≈ 0.5-1.5 m",
            "Flowers": "White, pink, red or purple; four petals",
            "Fruit": "Globular capsule (poppy head)",
            "Latex": "Milky white, darkens on air exposure",
            "Native region": "Eastern Mediterranean / South-West Asia",
            "Seeds": "Edible, used in baking and for poppy-seed oil",
        },
        "chemical": {
            "Morphine (≈ 8-14 % of dry opium)": "Phenanthrene alkaloid; strong analgesic",
            "Noscapine (≈ 4-8 %)": "Phthalideisoquinoline; cough suppressant, not analgesic",
            "Codeine (≈ 0.7-2.5 %)": "Phenanthrene alkaloid; mild analgesic, antitussive",
            "Papaverine (≈ 0.5-2.5 %)": "Benzylisoquinoline; smooth-muscle relaxant / vasodilator",
            "Thebaine (≈ 0.5-2 %)": "Phenanthrene alkaloid; not used directly as analgesic",
            "Mechanism (morphine)": "μ-opioid receptor agonist in brain and spinal cord",
            "Half-life (morphine)": "≈ 2-3 h",
            "Protein binding (morphine)": "≈ 30-35 %",
            "Metabolism (morphine)": "Liver glucuronidation; excreted mainly in urine",
        },
        "reactions": [
            ("Nature of alkaloids", "Basic nitrogen compounds that form water-soluble salts with acids."),
            ("Biosynthesis", "Plant builds them from the amino acid tyrosine via (S)-reticuline."),
            ("Meconic acid", "A characteristic acid of opium, used as a marker for its presence."),
            ("Latex ageing", "Fresh latex darkens to brown on oxidation."),
        ],
        "tests": [
            ("Meconic acid + FeCl3", "Red colour (classic identification of opium)"),
            ("Marquis reagent", "Purple-violet with morphine (presumptive test)"),
            ("Dragendorff's", "Orange precipitate (alkaloids)"),
            ("Confirmatory", "GC-MS or HPLC in a licensed laboratory"),
        ],
        "uses": ["Source of morphine and codeine (severe pain, cough)", "Papaverine for vasospasm and smooth-muscle relaxation",
                 "Noscapine as a cough suppressant", "Poppy seeds and oil in food (seeds can trigger a positive urine drug test)"],
        "safety": ("Opium and its alkaloids are controlled substances (UN Single Convention on Narcotic Drugs, 1961; "
                   "in India the NDPS Act, 1985). Cultivation and possession need a licence. Opioids can cause "
                   "respiratory depression, dependence and fatal overdose. In suspected overdose call emergency "
                   "services; naloxone reverses opioid effects. This page is for education only."),
        "cmp": {"Type": "Plant (natural source)", "Primary use": "Source of opioid medicines", "Mechanism": "μ-opioid receptor agonism (morphine)",
                "Legal status": "Controlled / licensed only", "num": (285.34, 2.5, 32.5)},
    },
}

NAMES = list(COMPOUNDS.keys())


def structure_url(cid: int) -> str:
    return f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=300x300"


def hud(label, value):
    cls = "hud-v s" if len(str(value)) > 16 else "hud-v"
    return f'<div class="hud"><div class="hud-l">{label}</div><div class="{cls}">{value}</div></div>'


# ---------------------------------------------------------------
# Sidebar + hero
# ---------------------------------------------------------------
st.sidebar.title("💊 Compound Explorer")
mode = st.sidebar.radio("Mode", ["Single compound", "Compare all"])
st.sidebar.markdown("---")
st.sidebar.caption("Typical literature values for education only. Not medical advice; verify in a pharmacopoeia, SDS or with a doctor.")

st.markdown(
    '<div class="hero"><h1>Pharma Compound Explorer</h1>'
    '<p>Molecular profiles of Paracetamol, Levocetirizine and the Opium poppy</p>'
    '<div class="nodes">'
    '<div class="node"><div class="hex a">1</div><span>Paracetamol: analgesic</span></div>'
    '<div class="node"><div class="hex b">2</div><span>Levocetirizine: antihistamine</span></div>'
    '<div class="node"><div class="hex c">3</div><span>Opium poppy: alkaloid source</span></div>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Single compound view
# ---------------------------------------------------------------
if mode == "Single compound":
    name = st.sidebar.selectbox("Choose a compound", NAMES)
    c = COMPOUNDS[name]

    left, right = st.columns([1, 2])
    with left:
        st.image(structure_url(c["cid"]), caption=f"{c['ids'][1][1] if name == 'Opium poppy' else name} structure (PubChem)")
    with right:
        st.header(name)
        st.markdown(f'<span class="pill">{c["class"]}</span>', unsafe_allow_html=True)
        st.write(c["description"])
        m1, m2 = st.columns(2)
        m1.markdown(hud("Formula", c["formula"]), unsafe_allow_html=True)
        m2.markdown(hud("Molar mass", c["mass"]), unsafe_allow_html=True)
        ids = "<br>".join(
            f"<b>{k}:</b> <code>{v}</code>" if k.endswith("SMILES") or "SMILES" in k else f"<b>{k}:</b> {v}"
            for k, v in c["ids"]
        )
        st.markdown(f'<div class="glass ids">{ids}</div>', unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["Physical / botanical", "Chemical & PK", "Reactions & tests", "Uses", "Safety"])

    with t1:
        df = pd.DataFrame([(k, "—" if v is None else str(v)) for k, v in c["physical"].items()], columns=["Property", "Value"])
        st.table(df.set_index("Property"))
    with t2:
        st.table(pd.DataFrame(list(c["chemical"].items()), columns=["Property", "Details"]).set_index("Property"))
    with t3:
        st.subheader("Chemistry notes" if name == "Opium poppy" else "Characteristic reactions")
        for title, text in c["reactions"]:
            st.markdown(f'<div class="rx"><b>{title}:</b> {text}</div>', unsafe_allow_html=True)
        st.subheader("Identification tests")
        st.table(pd.DataFrame(c["tests"], columns=["Test", "Observation"]).set_index("Test"))
    with t4:
        for u in c["uses"]:
            st.markdown(f"- {u}")
    with t5:
        st.warning(c["safety"])

# ---------------------------------------------------------------
# Comparison view
# ---------------------------------------------------------------
else:
    st.header("Compare compounds")
    rows = []
    for n, c in COMPOUNDS.items():
        m = c["cmp"]
        rows.append({"Compound": n, "Type": m["Type"], "Class": c["class"], "Primary use": m["Primary use"],
                     "Mechanism": m["Mechanism"], "Legal status": m["Legal status"]})
    st.table(pd.DataFrame(rows).set_index("Compound"))

    num = pd.DataFrame(
        {n: COMPOUNDS[n]["cmp"]["num"] for n in NAMES},
        index=["Molar mass (g/mol)", "Half-life (h)", "Protein binding (%)"],
    ).T
    prop = st.selectbox("Plot a property", list(num.columns))
    st.bar_chart(num[prop], color="#35f0d0")
    st.caption("Opium poppy values refer to its main alkaloid, morphine. Protein binding uses mid-range values (paracetamol 10-25 %, morphine 30-35 %).")

    st.subheader("Structures")
    cols = st.columns(len(NAMES))
    for col, n in zip(cols, NAMES):
        col.image(structure_url(COMPOUNDS[n]["cid"]), caption=n if n != "Opium poppy" else "Opium poppy (morphine)")
