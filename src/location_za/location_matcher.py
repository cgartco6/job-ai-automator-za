import re
from .provinces import SOUTH_AFRICA_PROVINCES, find_location_province

class LocationMatcher:
    def __init__(self):
        self.provinces = SOUTH_AFRICA_PROVINCES
    
    def add_custom_location(self, location_name: str, location_type: str = "town"):
        """AI-powered location addition with automatic province detection"""
        
        # Use AI to determine the best province match
        province_match = self._ai_determine_province(location_name)
        
        if province_match and province_match in self.provinces:
            # Add to the appropriate province
            if location_type == "city":
                self.provinces[province_match]['cities'].append(location_name)
            elif location_type == "town":
                self.provinces[province_match]['towns'].append(location_name)
            else:
                self.provinces[province_match]['villages'].append(location_name)
            
            # Remove duplicates and sort
            self.provinces[province_match]['cities'] = sorted(list(set(self.provinces[province_match]['cities'])))
            self.provinces[province_match]['towns'] = sorted(list(set(self.provinces[province_match]['towns'])))
            self.provinces[province_match]['villages'] = sorted(list(set(self.provinces[province_match]['villages'])))
            
            return {
                "success": True,
                "province": self.provinces[province_match]['name'],
                "province_code": province_match,
                "location_type": location_type
            }
        
        return {"success": False, "error": "Could not determine province"}
    
    def _ai_determine_province(self, location_name: str) -> str:
        """Use AI to determine which province a location belongs to"""
        # This would integrate with an AI service
        # For now, using pattern matching and known data
        
        location_lower = location_name.lower()
        
        # Gauteng patterns
        if any(word in location_lower for word in ['johannesburg', 'pretoria', 'sandton', 'randburg', 'roodepoort']):
            return "GP"
        
        # Western Cape patterns
        elif any(word in location_lower for word in ['cape town', 'stellenbosch', 'paarl', 'somerset']):
            return "WC"
        
        # KZN patterns
        elif any(word in location_lower for word in ['durban', 'pietermaritzburg', 'umhlanga', 'ballito']):
            return "KZN"
        
        # Add more patterns for other provinces...
        
        else:
            # Default to Gauteng for unknown locations
            return "GP"
