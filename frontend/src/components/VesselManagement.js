import React, { useState, useEffect } from 'react';
import { getVessels, createVessel, updateVessel, deleteVessel } from '../services/api'; // Ajusta la ruta
import Modal from 'react-modal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

Modal.setAppElement('#root');

function VesselsManagement() {
  const [vessels, setVessels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showVesselForm, setShowVesselForm] = useState(false);
  const [editingVessel, setEditingVessel] = useState(null);
  const [newVessel, setNewVessel] = useState({
    name: '',
    type: '',
    capacity: 0,
    description: '',
    is_active: true,
  });
  const [filterField, setFilterField] = useState('name');
  const [filterValue, setFilterValue] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [groupBy, setGroupBy] = useState(null);
  const [selectedVessels, setSelectedVessels] = useState({});
  const [allSelected, setAllSelected] = useState({});
  
  const Spacer = ({ width }) => <div style={{ width: `${width}rem`, display: 'inline-block' }}></div>;

  useEffect(() => {
    const fetchVessels = async () => {
      setLoading(true);
      try {
        const response = await getVessels();
        console.log("Respuesta de la API:", response);
        console.log("Datos de la API:", response.data);
        if (response && Array.isArray(response.data)) {
          setVessels(response.data);
        } else {
          setError("La respuesta de la API no es un array válido.");
          setVessels([]);
        }
      } catch (err) {
        setError(err);
        setVessels([]);
      } finally {
        setLoading(false);
      }
    };
    fetchVessels();
  }, []);

  const handleOpenVesselForm = (vessel = null) => {
    setEditingVessel(vessel);
    if (vessel) {
      setNewVessel({ ...vessel });
    } else {
      setNewVessel({ name: '', type: '', capacity: 0, description: '', is_active: true });
    }
    setShowVesselForm(true);
  };

  const handleCloseVesselForm = () => {
    setShowVesselForm(false);
    setEditingVessel(null);
  };

  const handleCreateOrUpdateVessel = async () => {
    try {
      if (editingVessel) {
        await updateVessel(editingVessel.id, {
          name: newVessel.name,
          type: newVessel.type,
          capacity: parseFloat(newVessel.capacity),
          description: newVessel.description,
          is_active: newVessel.is_active,
        });
      } else {
        await createVessel({
          name: newVessel.name,
          type: newVessel.type,
          capacity: parseFloat(newVessel.capacity),
          description: newVessel.description,
          is_active: newVessel.is_active,
        });
      }
      const response = await getVessels();
      if (response && Array.isArray(response.data)) {
        setVessels(response.data);
      } else {
        setError("La respuesta de la API no es un array válido.");
        setVessels([]);
      }
      handleCloseVesselForm();
    } catch (err) {
      setError(err);
    }
  };

  const handleDeleteVessel = async (id) => {
    try {
      await deleteVessel(id);
      const response = await getVessels(); // Cambia data por response para acceder a response.data
      if (response && Array.isArray(response.data)) {
        setVessels(response.data);
      } else {
        setError("La respuesta de la API no es un array válido.");
        setVessels([]);
      }
    } catch (err) {
      setError(err);
    }
  };

  const filteredVessels = vessels.filter((vessel) =>
    vessel[filterField].toLowerCase().includes(filterValue.toLowerCase())
  );

  const handleSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedVessels = [...filteredVessels].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];
    if (aValue < bValue) return sortConfig.direction === 'ascending' ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === 'ascending' ? 1 : -1;
    return 0;
  });

  const groupVessels = (data, groupBy) => {
    return data.reduce((acc, vessel) => {
      const key = vessel[groupBy];
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(vessel);
      return acc;
    }, {});
  };

  const groupedVessels = groupBy ? groupVessels(sortedVessels, groupBy) : { "Todas las Vasijas": sortedVessels };

  const handleSelectAll = (e, group) => {
    setAllSelected({ ...allSelected, [group]: e.target.checked });
    const updatedSelections = { ...selectedVessels };
    if (e.target.checked) {
      updatedSelections[group] = groupedVessels[group].map((vessel) => vessel.id);
    } else {
      updatedSelections[group] = [];
    }
    setSelectedVessels(updatedSelections);
  };

  const handleSelectVessel = (e, vessel, group) => {
    const groupSelections = selectedVessels[group] || [];
    const updatedSelections = e.target.checked
      ? [...groupSelections, vessel.id]
      : groupSelections.filter((id) => id !== vessel.id);
    setSelectedVessels({ ...selectedVessels, [group]: updatedSelections });

    const allGroupSelected = groupedVessels[group].every((s) => selectedVessels[group]?.includes(s.id));
    setAllSelected({ ...allSelected, [group]: allGroupSelected });
  };

  const generateCSV = () => {
    const selectedData = [];
    for (const group in selectedVessels) {
      const selectedIdsInGroup = selectedVessels[group];
      if (selectedIdsInGroup && selectedIdsInGroup.length > 0) {
        const filteredVessels = vessels.filter((vessel) => selectedIdsInGroup.includes(vessel.id));
        selectedData.push(...filteredVessels);
      }
    }
    if (selectedData.length === 0) {
      alert("No hay vasijas seleccionadas para descargar.");
      return;
    }
    const csvRows = [];
    const header = Object.keys(selectedData[0]).join(",");
    csvRows.push(header);
    selectedData.forEach((item) => {
      const values = Object.values(item).map((value) => `"${value}"`).join(",");
      csvRows.push(values);
    });
    const csvContent = csvRows.join("\r\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.setAttribute("download", "Vasijas.csv");
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) return <p>Cargando...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div className="container mx-auto p-4">
      <div className="table-header">
        <button onClick={() => handleOpenVesselForm()} className="btn btn-primary">Crear Vasija</button>
        <Spacer width={0.5} />
        {Object.values(selectedVessels).flat().length > 0 && (
          <button className="btn btn-secondary" onClick={generateCSV}>Descargar CSV</button>
        )}
      </div>
      <div className="flex gap-2 mb-4">
        <label htmlFor="groupingField" className="mr-2">Agrupar por:</label>
        <Spacer width={0.2} />
        <select id="groupingField" value={groupBy || "none"} onChange={(e) => setGroupBy(e.target.value === "none" ? null : e.target.value)} className="border p-2 rounded">
          <option value="none">Sin Agrupación</option>
          <option value="type">Tipo</option>
          <option value="capacity">Capacidad</option>
        </select>
      <Spacer width={2} />
        <select value={filterField} onChange={(e) => setFilterField(e.target.value)} className="border p-2 rounded">
          <option value="name">Nombre</option>
          <option value="type">Tipo</option>
          <option value="capacity">Capacidad</option>
        </select>
        <Spacer width={0.2} />
        <input type="text" value={filterValue} onChange={(e) => setFilterValue(e.target.value)} placeholder={`Buscar por ${filterField}...`} className="border p-2 rounded w-64" />
      </div>
  
      {Object.entries(groupedVessels).map(([group, vessels]) => (
        <div key={group} className="mb-4">
          {groupBy && <h3 className="titulo-seccion">{`${groupBy.charAt(0).toUpperCase() + groupBy.slice(1).replace("_", " ")}: ${group}`}</h3>}
          <table className="table-auto w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border border-gray-300 p-2">
                  <input type="checkbox" checked={allSelected[group] || false} onChange={(e) => handleSelectAll(e, group)} />
                </th>
                <th className="border border-gray-300 p-2" onClick={() => handleSort('name')}>Nombre</th>
                <th className="border border-gray-300 p-2" onClick={() => handleSort('type')}>Tipo</th>
                <th className="border border-gray-300 p-2" onClick={() => handleSort('capacity')}>Capacidad</th>
                <th className="border border-gray-300 p-2">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {vessels.map((vessel) => (
                <tr key={vessel.id}>
                  <td className="border border-gray-300 p-2">
                    <input type="checkbox" checked={selectedVessels[group]?.includes(vessel.id) || false} onChange={(e) => handleSelectVessel(e, vessel, group)} />
                  </td>
                  <td className="border border-gray-300 p-2">{vessel.name}</td>
                  <td className="border border-gray-300 p-2">{vessel.type}</td>
                  <td className="border border-gray-300 p-2">{vessel.capacity}</td>
                  <td className="border border-gray-300 p-2">
                    <button onClick={() => handleOpenVesselForm(vessel)}
                      className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 mr-2">
                      <FontAwesomeIcon icon={faSearch} />
                    </button>
                    <button onClick={() => handleDeleteVessel(vessel.id)} className="bg-red-500 text-white p-2 rounded hover:bg-red-600">Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
  
      <Modal isOpen={showVesselForm} onRequestClose={handleCloseVesselForm} className="modal-content" overlayClassName="modal-overlay" contentLabel="Crear/Editar Vasija">
        <div className="modal-wrapper">
          <div className="modal-content">
            <h2 className="modal-title">{editingVessel ? 'Editar Vasija' : 'Crear Vasija'}</h2>
            <div className="modal-form-grid">
              <div className="modal-column">
                <div className="mb-4">
                  <label className="modal-form-label">Nombre:</label>
                  <input type="text" value={newVessel.name} onChange={(e) => setNewVessel({ ...newVessel, name: e.target.value })} className="modal-form-input" />
                </div>
                <div className="mb-4">
                  <label className="modal-form-label">Descripción:</label>
                  <textarea value={newVessel.description} onChange={(e) => setNewVessel({ ...newVessel, description: e.target.value })} className="modal-form-input" />
                </div>
                <div className="mb-4">
                  <label className="modal-form-label">Activo:</label>
                  <input type="checkbox" checked={newVessel.is_active} onChange={(e) => setNewVessel({ ...newVessel, is_active: e.target.checked })} className="modal-form-input" />
                </div>
              </div>
              <div className="modal-column">
                <div className="mb-4">
                  <label className="modal-form-label">Tipo:</label>
                  <input type="text" value={newVessel.type} onChange={(e) => setNewVessel({ ...newVessel, type: e.target.value })} className="modal-form-input" />
                </div>
                <div className="mb-4">
                  <label className="modal-form-label">Capacidad:</label>
                  <input type="number" value={newVessel.capacity} onChange={(e) => setNewVessel({ ...newVessel, capacity: e.target.value })} className="modal-form-input" />
                </div>
              </div>
            </div>
            <div className="modal-buttons mt-4">
              <button onClick={handleCloseVesselForm} className="btn btn-secondary">Cancelar</button>
              <button onClick={handleCreateOrUpdateVessel} className="btn btn-primary">{editingVessel ? 'Actualizar' : 'Crear'}</button>
            </div>
          </div>
        </div>
      </Modal>
    </div>
  );
}

export default VesselsManagement