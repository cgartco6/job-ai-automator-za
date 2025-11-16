import React, { useState, useEffect } from 'react';

const LocationDropdown = ({ onLocationChange }) => {
    const [provinces, setProvinces] = useState({});
    const [selectedProvince, setSelectedProvince] = useState('');
    const [selectedCity, setSelectedCity] = useState('');
    const [customLocation, setCustomLocation] = useState('');

    useEffect(() => {
        // Load South Africa location data
        fetch('/api/locations/za')
            .then(response => response.json())
            .then(data => setProvinces(data));
    }, []);

    const handleCustomLocation = async () => {
        if (customLocation.trim()) {
            const response = await fetch('/api/locations/custom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location: customLocation })
            });
            const result = await response.json();
            if (result.success) {
                alert(`Location added to ${result.province}`);
                setCustomLocation('');
            }
        }
    };

    return (
        <div className="location-selector">
            <div className="form-group">
                <label>Province:</label>
                <select 
                    value={selectedProvince} 
                    onChange={(e) => setSelectedProvince(e.target.value)}
                    className="form-control"
                >
                    <option value="">Select Province</option>
                    {Object.keys(provinces).map(provinceCode => (
                        <option key={provinceCode} value={provinceCode}>
                            {provinces[provinceCode].name}
                        </option>
                    ))}
                </select>
            </div>

            {selectedProvince && (
                <div className="form-group">
                    <label>City/Town:</label>
                    <select 
                        value={selectedCity} 
                        onChange={(e) => {
                            setSelectedCity(e.target.value);
                            onLocationChange(selectedProvince, e.target.value);
                        }}
                        className="form-control"
                    >
                        <option value="">Select Location</option>
                        {provinces[selectedProvince]?.cities.map(city => (
                            <option key={city} value={city}>{city}</option>
                        ))}
                        {provinces[selectedProvince]?.towns.map(town => (
                            <option key={town} value={town}>{town}</option>
                        ))}
                    </select>
                </div>
            )}

            <div className="form-group">
                <label>Can't find your town? Add it here:</label>
                <div className="input-group">
                    <input
                        type="text"
                        value={customLocation}
                        onChange={(e) => setCustomLocation(e.target.value)}
                        placeholder="Enter your town or village"
                        className="form-control"
                    />
                    <button 
                        onClick={handleCustomLocation}
                        className="btn btn-primary"
                    >
                        Add Location
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LocationDropdown;
