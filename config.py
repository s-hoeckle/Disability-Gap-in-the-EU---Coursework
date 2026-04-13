TEAL_PALETTE = {
    "teal_1": "#b5d1ae",
    "teal_2": "#80ae9a",
    "teal_3": "#568b87",
    "teal_4": "#326b77",
    "teal_5": "#1b485e",
    "teal_6": "#122740",
}


COLORS = {
    "NONE": TEAL_PALETTE["teal_6"],
    "SOME": TEAL_PALETTE["teal_4"],
    "SEV": TEAL_PALETTE["teal_1"],
    "SM_SEV": TEAL_PALETTE["teal_4"],
    "GAP_TEXT": TEAL_PALETTE["teal_4"],
}


PLOT_SETTINGS = {
    "figsize": (15, 10),
    "group_spacing": 1.3,
    "bar_height": 0.25,
    "bar_height_gap": 0.35,
}


FILES = {
    "gbv_any": "data/estat_gbv_any_lim.tsv",
    "education": "data/estat_edat_lfs_9920.tsv",
    "health": "data/estat_hlth_dpe010.tsv",
}


SEVERITY_LEVELS = ["TOTAL", "SOME", "SEV", "SM_SEV", "NONE"]
EXCLUDED_GEO = ["EU_V"]


EDU_CONFIG = {
    "target_age": "Y15-74",
    "fallback_age": "Y15-64",
    "tet_level": "ED5-8",
    "prim_level": "ED0-2",
    "disability_code": "SM_SEV",
    "able_code": "NONE",
}
