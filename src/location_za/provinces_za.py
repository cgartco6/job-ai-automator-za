SOUTH_AFRICA_PROVINCES = {
    "GP": {
        "name": "Gauteng",
        "cities": ["Johannesburg", "Pretoria", "Sandton", "Randburg", "Roodepoort", "Centurion", "Midrand"],
        "towns": ["Alberton", "Kempton Park", "Boksburg", "Benoni", "Springs", "Germiston", "Vereeniging"],
        "villages": ["Irene", "Hartbeespoort", "Cullinan", "Bronkhorstspruit"]
    },
    "WC": {
        "name": "Western Cape",
        "cities": ["Cape Town", "Stellenbosch", "Paarl", "Worcester", "George", "Mossel Bay"],
        "towns": ["Somerset West", "Bellville", "Kuils River", "Parow", "Mitchells Plain", "Khayelitsha"],
        "villages": ["Hout Bay", "Simon's Town", "Strand", "Gordon's Bay", "Plettenberg Bay"]
    },
    "KZN": {
        "name": "KwaZulu-Natal",
        "cities": ["Durban", "Pietermaritzburg", "Richards Bay", "Newcastle", "Ladysmith"],
        "towns": ["Umhlanga", "Ballito", "Amanzimtoti", "Margate", "Scottburgh", "Port Shepstone"],
        "villages": ["Salt Rock", " Sheffield Beach", "Pennington", "Hibberdene"]
    },
    "EC": {
        "name": "Eastern Cape",
        "cities": ["Port Elizabeth", "East London", "Mthatha", "Graaff-Reinet"],
        "towns": ["Uitenhage", "Queenstown", "Grahamstown", "Butterworth", "Cradock"],
        "villages": ["St Francis Bay", "Jeffrey's Bay", "Port Alfred", "Hogsback"]
    },
    "FS": {
        "name": "Free State",
        "cities": ["Bloemfontein", "Welkom", "Bethlehem", "Kroonstad"],
        "towns": ["Sasolburg", "Virginia", "Harrismith", "Phuthaditjhaba"],
        "villages": ["Clarens", "Ficksburg", "Parys", "Rosendal"]
    },
    "MP": {
        "name": "Mpumalanga",
        "cities": ["Nelspruit", "Witbank", "Middleburg", "Secunda"],
        "towns": ["Barberton", "Pilgrim's Rest", "Hazyview", "Malelane"],
        "villages": ["Sabie", "Graskop", "Dullstroom", "Kaapsehoop"]
    },
    "NW": {
        "name": "North West",
        "cities": ["Mahikeng", "Potchefstroom", "Klerksdorp", "Rustenburg"],
        "towns": ["Brits", "Zeerust", "Wolmaransstad", "Vryburg"],
        "villages": ["Hartbeesfontein", "Coligny", "Groot Marico"]
    },
    "LP": {
        "name": "Limpopo",
        "cities": ["Polokwane", "Thohoyandou", "Tzaneen", "Lephalale"],
        "towns": ["Mokopane", "Bela-Bela", "Makhado", "Giyani"],
        "villages": ["Haenertsburg", "Modjadjiskloof", "Ofcolaco"]
    },
    "NC": {
        "name": "Northern Cape",
        "cities": ["Kimberley", "Upington", "Springbok", "De Aar"],
        "towns": ["Kuruman", "Kathu", "Postmasburg", "Pofadder"],
        "villages": ["Augrabies", "McGregor", "Noupoort"]
    }
}

def get_all_locations():
    """Return all locations in South Africa"""
    all_locations = []
    for province_code, province_data in SOUTH_AFRICA_PROVINCES.items():
        all_locations.extend(province_data['cities'])
        all_locations.extend(province_data['towns'])
        all_locations.extend(province_data['villages'])
    return sorted(list(set(all_locations)))

def find_location_province(location_name):
    """Find which province a location belongs to"""
    for province_code, province_data in SOUTH_AFRICA_PROVINCES.items():
        if (location_name in province_data['cities'] or 
            location_name in province_data['towns'] or 
            location_name in province_data['villages']):
            return province_code, province_data['name']
    return None, None
