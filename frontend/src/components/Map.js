import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import * as wellknown from 'wellknown';

const latitudCentral = -34.6037;
const longitudCentral = -58.3816;

const Map = ({ parcela }) => {
    const mapRef = useRef(null);

    useEffect(() => {
        if (mapRef.current === null) {
            mapRef.current = L.map('map').setView([latitudCentral, longitudCentral], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mapRef.current);
        }

        if (parcela && parcela.geom) {
            try {
                const geojson = wellknown.toGeoJSON(parcela.geom);
                if (geojson) {
                    L.geoJSON(geojson).addTo(mapRef.current);

                    const bounds = L.geoJSON(geojson).getBounds();
                    if (bounds.isValid()) {
                        mapRef.current.fitBounds(bounds);
                    } else {
                        console.warn("Límites inválidos, centrado en la primera coordenada:", geojson.coordinates[0]);
                        if (geojson.type === "Point") {
                            mapRef.current.setView(geojson.coordinates, 13);
                        } else if (geojson.type === "LineString") {
                            mapRef.current.setView(geojson.coordinates[0], 13);
                        } else if (geojson.type === "Polygon") {
                            mapRef.current.setView(geojson.coordinates[0][0], 13);
                        }
                    }
                } else {
                    console.warn("WKT inválido o conversión fallida:", parcela.geom);
                }
            } catch (error) {
                console.error("Error al convertir WKT a GeoJSON:", error);
            }
        } else {
            console.warn("La parcela o la geometría no están definidas.");
        }

        return () => {
            if (mapRef.current) {
                mapRef.current.remove();
                mapRef.current = null;
            }
        };
    }, [parcela]);

    return <div id="map" style={{ height: '400px', width: '100%' }}></div>;
};

export default Map;