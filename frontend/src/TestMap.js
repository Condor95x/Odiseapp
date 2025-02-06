import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import * as wellknown from 'wellknown';

const TestMap = () => {
    const mapRef = useRef(null);
    const wkt = "POLYGON ((-68.122 -31.52, -68.12 -31.5185, -68.119 -31.521, -68.1215 -31.523, -68.122 -31.52))"; // Geometría fija

    useEffect(() => {
        if (mapRef.current === null) {
            mapRef.current = L.map('test-map').setView([-31.52, -68.12], 13); // Coordenadas aproximadas
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mapRef.current);
        }

        try {
            const geojson = wellknown.toGeoJSON(wkt);
            if (geojson) {
                L.geoJSON(geojson).addTo(mapRef.current);
                const bounds = L.geoJSON(geojson).getBounds();
                if (bounds.isValid()) {
                    mapRef.current.fitBounds(bounds);
                } else {
                    console.warn("Geometría inválida, no se pueden calcular los límites.");
                }
            } else {
                console.warn("Error al convertir WKT a GeoJSON. Revisa el formato WKT.");
            }
        } catch (error) {
            console.error("Error al convertir WKT a GeoJSON:", error);
        }

        return () => {
            if (mapRef.current) {
                mapRef.current.remove();
                mapRef.current = null;
            }
        };
    }, []);

    return <div id="test-map" style={{ height: '400px', width: '100%' }}></div>;
};

export default TestMap;