SOUTH_AFRICA_REGIONS = {
    "GP": {
        "regions": {
            "johannesburg": ["Johannesburg", "Sandton", "Randburg", "Roodepoort", "Soweto"],
            "pretoria": ["Pretoria", "Centurion", "Midrand", "Akasia"],
            "ekurhuleni": ["Alberton", "Kempton Park", "Boksburg", "Benoni", "Germiston"]
        }
    },
    "WC": {
        "regions": {
            "cape_town": ["Cape Town", "Bellville", "Mitchells Plain", "Khayelitsha"],
            "winelands": ["Stellenbosch", "Paarl", "Franschhoek", "Wellington"],
            "garden_route": ["George", "Mossel Bay", "Knysna", "Plettenberg Bay"]
        }
    },
    "KZN": {
        "regions": {
            "durban": ["Durban", "Umhlanga", "Pinetown", "Amanzimtoti"],
            "north_coast": ["Ballito", "Salt Rock", "Tongaat"],
            "south_coast": ["Scottburgh", "Port Shepstone", "Margate"]
        }
    },
    "EC": {
        "regions": {
            "nelson_mandela_bay": ["Port Elizabeth", "Uitenhage", "Despatch"],
            "east_london": ["East London", "Mdantsane", "Cambridge"],
            "wild_coast": ["Mthatha", "Butterworth", "Idutywa"]
        }
    },
    "FS": {
        "regions": {
            "mangaung": ["Bloemfontein", "Botshabelo", "Thaba Nchu"],
            "goldfields": ["Welkom", "Virginia", "Allanridge"],
            "northern_fs": ["Kroonstad", "Sasolburg", "Parys"]
        }
    },
    "MP": {
        "regions": {
            "lowveld": ["Nelspruit", "White River", "Hazyview"],
            "highveld": ["Witbank", "Middleburg", "Secunda"],
            "south_west": ["Ermelo", "Piet Retief", "Amsterdam"]
        }
    },
    "NW": {
        "regions": {
            "bojanala": ["Rustenburg", "Brits", "Thabazimbi"],
            "central": ["Mahikeng", "Lichtenburg", "Zeerust"],
            "southern": ["Potchefstroom", "Klerksdorp", "Stilfontein"]
        }
    },
    "LP": {
        "regions": {
            "capricorn": ["Polokwane", "Mankweng", "Seshego"],
            "mopani": ["Tzaneen", "Giyani", "Phalaborwa"],
            "vhembe": ["Thohoyandou", "Makhado", "Musina"]
        }
    },
    "NC": {
        "regions": {
            "diamond_fields": ["Kimberley", "Barkly West", "Warrenton"],
            "kalahari": ["Upington", "Kathu", "Kuruman"],
            "namaqualand": ["Springbok", "Pofadder", "Port Nolloth"]
        }
    }
}

def get_region_for_location(location_name: str, province_code: str) -> str:
    """Get the region for a specific location"""
    if province_code not in SOUTH_AFRICA_REGIONS:
        return "unknown"
    
    location_lower = location_name.lower()
    for region_name, locations in SOUTH_AFRICA_REGIONS[province_code]["regions"].items():
        for loc in locations:
            if location_lower in loc.lower() or loc.lower() in location_lower:
                return region_name
    return "other"
