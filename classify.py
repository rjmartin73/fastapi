import pandas as pd
import re
import numpy as np
import json

date_pattern = re.compile(r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}|\d{2}[-/]\d{2}[-/]\d{2})\b')
# Conduit
conduit_terms = {'cndt', 'conduit', 'emt', 'ent', 'flex', 'grc', 'pipe', 'pvc', 'smurf', 'sealtight', 'cond'}
ent_terms = ['ent', 'smurf']
emt_terms = ['emt', "thinwall", "thin wall"]
grc_terms = ['grc', 'rmc', 'steel', 'galv', 'imc']
pvc_terms = ['pvc', 'rigid', 'ridgid', 'ridig', 'sch']
flex_terms = ['flex', 'carflex', 'sealtight', 'seal tight', 'liquid', 'liq tite', 'liq-tite', "lfmc", 'frt', 'nmlt']
conduit_exclude_terms = {
    '100A', '110A', '120A', '130A', '140A', '150A', '160A', '170A', '180A', '190A', '200A', '20A', '30A',
    '401', '40A', '45', '50A', '60A', '70A', '80A', '90', '90A', 'accent', 'acorn', 'adap', 'adapt', 'assem',
    'assembly', 'back', 'bell', 'bender', 'blow', 'body', 'box', 'branch', 'brush', 'bulb', 'bush', 'cadd',
    'caddy', 'calmp', 'camera', 'can', 'cap', 'center', 'century', 'chair', 'changeover', 'city', 'cla',
    'clam', 'clamp', 'clip', 'collar', 'comp', 'conen', 'conn', 'coul', 'coup', 'cover', 'cplg', 'crimp',
    'cutter', 'degree', 'dent', 'dfac', 'die', 'elbow', 'entry', 'equip', 'ext', 'fee', 'female', 'fit',
    'flange', 'gallon', 'gang', 'glue', 'groun', 'ground', 'hang', 'heater', 'hous', 'hngr', 'hub', 'insta', 'insul',
    'lift', 'light', 'lock', 'lub', 'lug', 'male', 'marker', 'material', 'measur', 'ment', 'mount', 'nipp',
    'nut', 'offset', 'oil', 'order', 'paint', 'pen', 'pencil', 'piston', 'plug', 'presentation', 'raceway',
    'ream', 'recept', 'recess', 'rent', 'repair', 'return', 'rework', 'rig ', 'rod', 'sand', 'saw', 'sconce',
    'screw', 'service', 'set', 'sharpie', 'sleeve', 'slv', 'stand', 'stapl', 'srap', 'stap', 'stra', 'strap', 'strut', 'stub',
    'supp', 'suppo', 'support', 't8', 'tape', 'tent', 'term', 'tie', 'toglock', 'tower', 'tray', 'vent',
    'vise', 'watt', 'wrap', 'pick', 'ball', 'spray', 'reduc', 'xentry', 'flouresc', 'mitsubishi', 'snap', 'enclosure',
    'oz', 'weather head', 'weatherhed', 'install', 'ush', 'unload', 'fluor', 'space', 'scent', 'cpl', 'temflex', 'cross',
    ' fa', ' ma ', 'ma,', 'male', 'fema', 'bolt', 'hole', 'putty', 'flexpro', 'concrete', 'bonding', 'agent', 'heat' 'gun',
    'seal off', 'outlet', 'price'} 
size_patterns = {
    '3-1/2"': re.compile(r'(?<!\d)3[-| ]1/2(?!\d)'),
    '2-1/2"': re.compile(r'(?<!\d)2[-| ]1/2(?!\d)'),
    '1-3/4"': re.compile(r'(?<!/d)1[-| ]3/4(?!\d)'),
    '1-1/2"': re.compile(r'(?<!\d)1[-| ]1/2(?!\d)'),
    '1-1/4"': re.compile(r'(?<!\d)1[-| ]1/4(?!\d)'),
    '3/4"': re.compile(r'(?<!\d)3/4(?!\d)'),
    '1/2"': re.compile(r'(?<!\d)1/2(?!\d)'),
    '6"': re.compile(r'(?<!\d)6[”|"|in| |.]|(?<!\d)6$'),
    '5"': re.compile(r'(?<!\d)5[”|"|in| |.]|(?<!\d)5$'),
    '4"': re.compile(r'(?<!\d)4[”|"|in| |.]|(?<!\d)4$'),
    '3"': re.compile(r'(?<!\d)3[”|"|in| |.]|(?<!\d)3$'),
    '2"': re.compile(r'(?<!\d)2[”|"|in| |.]|(?<!\d)2$'),
    '1"': re.compile(r'(?<!\d)1[”|"|-|in|\s|.]?|(?<!\d)1$',re.IGNORECASE),
}

# Wire
wire_terms = {
    'wire', 'cable', 'thhn', 'xhhw', 'awg', 'stranded', 'thw', 'romex', '12/2', '14/2', '20a', '30a', '4/0',
    '#10', '# 10', '12/4', '#12', '# 12', '#14', '# 14', '#16', 'cat5', 'cat6', '8/2', '6/2'}
wire_exclude_terms = {
    '100A', '110A', '120A', '15A', '20A', '30A', '40A', '50A', '60A', '70A', '80A', '90A', 'TY275M', 'adapter',
    'anchor', 'bolt', 'book', 'box', 'bracket', 'break', 'cap', 'clamp', 'clip', 'conn', 'connector', 'cover', 'cutter',
    'duct', 'fault', 'fuse', 'hanger', 'head', 'hngr', 'jumper', 'kit', 'lug', 'marker', 'nut', 'nvent', 'paint', 'photocell',
    'plate', 'pull', 'push', 'racetrack', 'rcpt', 'recept', 'screw', 'screws', 'square', 'strap', 'stud', 'switch',
    'tap', 'tapcon', 'tie', 'tray', 'tug', 'washer', 'wireway', 'install', 'ush', 'unload', 'wiremold', 'mold', 'alert', 'wired',
    'lube', 'reduc', 'dimmer', 'hold', 'riser', 'bit', 'pigtail', 'bend', 'phillip', ' ma ', 'ma,', ' fa', 'term', 'ship', 'crimp',
    'pin ', 'offset', 'conduit', 'emt', 'transit', 'support', 'gutter', 'scissor', 'pig', 'grd', 'southwire', 'stack'}
wire_types = {
    "WIRE THHN/XHHW/OTHER": re.compile(r'(?<!\w)?(?:thhn|xhhw|bare|uf)(?:[a-zA-Z\s_/.-]?|$)', re.IGNORECASE),
    "MC/ROMEX CABLE": re.compile(r'(?<!\w)?(?:cable|romex|ser)(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "LOW VOLTAGE CABLE": re.compile(r'(?<!\w)?(?:low voltage|cat|rj)(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE)
}
wire_sizes = {
    "#4/0": re.compile(r'(?<!\w)?#?(_4\/\d)', re.IGNORECASE),
    "#3/0": re.compile(r'(?<!\w)#?3/0(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#2/0": re.compile(r'(?<!\w)#?2/0(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#1/0": re.compile(r'(?<!\w)#?1/0(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#750": re.compile(r'(?<!\w)#?750(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#600": re.compile(r'(?<!\w)#?600(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#500": re.compile(r'(?<!\w)#?500(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#400": re.compile(r'(?<!\w)#?400(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#350": re.compile(r'(?<!\w)#?350(?:KCMIL|mcm|(?=[a-zA-Z]))?', re.IGNORECASE),
    "#300": re.compile(r'(?<!\w)#?300(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#250": re.compile(r'(?<!\w)?#?250(?:KCMIL|mcm|str)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#14": re.compile(r'(?<!\w)#?14(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#12": re.compile(r'(?<!\w)?#?12(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#10": re.compile(r'(?<!\w)#?10(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#8": re.compile(r'(?<!\w)#?8(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#6": re.compile(r'(?<!\w)#?6(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#4": re.compile(r'(?<!\w)#?4(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#3": re.compile(r'(?<!\w)#?3(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#2": re.compile(r'(?<!\w)#?2(?:KCMIL|mcm)(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "#1": re.compile(r'(?<!\w)#?1(?!/0)(?:KCMIL|mcm)?(?=[a-zA-Z\s_/.-]|$)', re.IGNORECASE),
    "LOW VOLTAGE": re.compile(r'\b(?:low\s*voltage|cat[56][E]?|romex|fplr|["|#]?16|18)\b', re.IGNORECASE)
}


# Step 1
def classify_item(description):
    if isinstance(description, str) and date_pattern.search(description) is None:
        desc_lower = description.lower()
        if any(term.lower() in desc_lower for term in wire_terms) and not any(term.lower() in desc_lower for term in wire_exclude_terms):
            return 'wire'
        elif any(term in desc_lower for term in conduit_terms) and not any(term in desc_lower for term in conduit_exclude_terms):
            return 'conduit'
    return 'exclude'


# Step 2: conduit
def classify_conduit(description):
    if isinstance(description, str) and date_pattern.search(description) is None:
        desc_lower = description.lower()
        if any(term in desc_lower for term in ent_terms):
            return 'CONDUIT - ENT'
        elif any(term in desc_lower for term in flex_terms):
            return 'CONDUIT - FLEX'
        elif any(term in desc_lower for term in emt_terms):
            return 'CONDUIT - EMT'
        elif any(term in desc_lower for term in grc_terms):
            return 'CONDUIT - GRC'
        elif any(term in desc_lower for term in pvc_terms):
            return 'CONDUIT - PVC'
        else:
            return 'UNK'


# Step 3: conduit
def get_conduit_size(description):
    description = description.replace("- ", " ").replace(" -", " ") 
    for size, pattern in size_patterns.items():
        if pattern.search(description):
            return f'{size}'  # ✅ Correctly returns the first match
    return 'UNK'  # ✅ Returns UNK only if no match is found


# Step 3: wire
def wire_type(description):
    description = description.lower()
    for type, pattern in wire_types.items():
        if pattern.search(description):
            return type
    return 'N/A'


# Step 2: wire
def get_wire_gauge(description):
    description = description.lower()
    for gauge, pattern in wire_sizes.items():
        if pattern.search(description):
            return f'{gauge}' # ✅ Correctly returns the first match
    return 'UNK'  # ✅ Returns UNK only if no match is found       


# Main method
def classify_main(df):
    # Ensure column names are correct
    if "Description" not in df.columns:
        raise ValueError("Missing 'Description' column in the input data.")

    # Step 1: Classify as Conduit, Wire, or Exclude
    df['MainCategory'] = df['Description'].apply(classify_item).str.upper()
    
    # Step 2: Classify SubCategory
    df['SubCategory'] = np.where(
        df['MainCategory'].str.contains('CONDUIT'),
        df['Description'].apply(classify_conduit),
        np.where(
            df['MainCategory'].str.contains('WIRE'),
            df['Description'].apply(wire_type),
            'N/A'
        ))

    # Step 3: Determine Size
    df['Size'] = np.where(
        df['MainCategory'].str.contains('CONDUIT'),
        df['Description'].apply(get_conduit_size),
        np.where(
            df['MainCategory'].str.contains('WIRE'),
            df['Description'].apply(get_wire_gauge),
            'N/A'
        )
    )

    # Step 4: Generate Final Label
    df['FinalLabel'] = np.where(
        df['MainCategory'].str.contains('CONDUIT'),
        df['Size'] + ' ' + df['SubCategory'],
        np.where(
            df['MainCategory'].str.contains('WIRE'),
            df['Size'] + ' ' + df['Description'].apply(wire_type),
            'N/A'
        )
    )

    # Convert to JSON format
    return {"results": df.to_dict(orient="records")}
