import React, { useState, useEffect } from "react";
import { getParcelas, createParcela, updateParcela, deleteParcela } from "../services/api"; // Asegúrate de importar la función correcta
import Papa from "papaparse";

const TableParcelas = () => {
  const [parcelas, setParcelas] = useState([]);
  const [selectedParcelas, setSelectedParcelas] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newParcela, setNewParcela] = useState({ nombre: "", cultivo: "", geom:"" }); // Sin "geom"
  const [editingParcela, setEditingParcela] = useState(null); // Estado para la edición
  const [sortConfig, setSortConfig] = useState({ key: "id", direction: "asc" }); // 🔼 Estado para ordenación
  const [filterField, setFilterField] = useState("nombre"); // Campo seleccionado
  const [filterValue, setFilterValue] = useState(""); // Valor ingresado por el usuario

  useEffect(() => {
    const fetchParcelas = async () => {
      const data = await getParcelas();
      setParcelas(data);
    };
    fetchParcelas();
  }, []);

  const filteredParcelas = parcelas.filter((p) => {
    if (!filterValue) return true; // Si no hay filtro, mostrar todas
  
    const value = String(p[filterField] || "").toLowerCase(); // Convierte a string y minúsculas
    return value.includes(filterValue.toLowerCase());
  });

  const sortedParcelas = [...filteredParcelas].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1;
    if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1;
    return 0;
  });

  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "asc" ? "desc" : "asc",
    }));
  };

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedParcelas(parcelas.map((parcela) => parcela.id));
    } else {
      setSelectedParcelas([]);
    }
  };

  const handleSelect = (id) => {
    setSelectedParcelas((prev) =>
      prev.includes(id) ? prev.filter((selectedId) => selectedId !== id) : [...prev, id]
    );
  };

  const handleEdit = () => {
    if (selectedParcelas.length === 1) {
      const parcelaToEdit = parcelas.find((p) => p.id === selectedParcelas[0]);
      if(parcelaToEdit){
      setEditingParcela({
        id: parcelaToEdit.id || "",
        nombre: parcelaToEdit.nombre || "",
        cultivo: parcelaToEdit.cultivo || "",
        geom: parcelaToEdit.geom || "", // ✅ Evita valores undefined
      });
    } else {
      console.error("No se encontró la parcela con el id seleccionado");
    }
  } else {
    console.warn("Se debe seleccionar una sola parcela");
  }
};

const handleUpdateParcela = async () => {
  if (!editingParcela) return;

  try {
      const updatedParcela = await updateParcela(editingParcela.id, editingParcela);
      setParcelas(parcelas.map((p) => (p.id === editingParcela.id ? updatedParcela : p)));
      setEditingParcela(null); // Cerrar formulario de edición
      setSelectedParcelas([]); // Deseleccionar la parcela editada
  } catch (error) {
      console.error("Error al actualizar la parcela:", error);
      alert("Error al actualizar la parcela.");
  }
};

  const handleDownloadCSV = () => {
    const selectedData = parcelas.filter((p) => selectedParcelas.includes(p.id));
    const csv = Papa.unparse(selectedData);
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "parcelas.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleCreateParcela = async () => {
    if (!newParcela.nombre || !newParcela.cultivo) {
      alert("Por favor, completa los campos obligatorios: Nombre y Cultivo.");
      return;
    }

    // Enviar solo nombre y cultivo (sin geom)
    const parcelaData = {
      nombre: newParcela.nombre,
      cultivo: newParcela.cultivo,
      geom: newParcela.geom || null, // Un GeoJSON de ejemplo,
    };

    console.log("Enviando datos:", JSON.stringify(parcelaData, null, 2)); // 👀 Ver qué datos se envían

    try {
      const response = await createParcela(parcelaData);
      console.log("Respuesta del servidor:", response); // Verificar la respuesta

      setParcelas([...parcelas, response]);
      setNewParcela({ nombre: "", cultivo: "" }); // Restablecer campos
      setShowForm(false);
    } catch (error) {
      console.error("Error al crear la parcela:", error);
      alert(`Error al crear parcela: ${error.message}`);
    }
  };

  const handleDeleteParcelas = async () => {
    if (selectedParcelas.length === 0) {
      alert("Por favor, selecciona al menos una parcela para eliminar.");
      return;
    }

    if (window.confirm("¿Estás seguro de que deseas eliminar las parcelas seleccionadas?")) {
      try {
        for (const id of selectedParcelas) {
          await deleteParcela(id);
        }
        // Recargar las parcelas después de eliminar
        const data = await getParcelas();
        setParcelas(data);
        setSelectedParcelas([]); // Limpiar la selección
        alert("Parcelas eliminadas exitosamente.");
      } catch (error) {
        console.error("Error al eliminar las parcelas:", error);
        alert("Error al eliminar las parcelas.");
      }
    }
  };

  return (
    <div className="container mx-auto p-4">
      {/* Botón para crear una nueva parcela */}
      <div className="flex justify-between items-center mb-4">
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Crear Nueva Parcela
        </button>
      </div>

      <div className="flex gap-2 mb-4">
  {/* Selector de campo */}
  <select
    value={filterField}
    onChange={(e) => setFilterField(e.target.value)}
    className="border p-2 rounded"
  >
    <option value="id">ID</option>
    <option value="nombre">Nombre</option>
    <option value="cultivo">Cultivo</option>
    <option value="area">Área</option>
  </select>

  {/* Input para valor de búsqueda */}
  <input
    type="text"
    value={filterValue}
    onChange={(e) => setFilterValue(e.target.value)}
    placeholder={`Buscar por ${filterField}...`}
    className="border p-2 rounded w-64"
  />
</div>

      {/* Tabla */}
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 p-2">
              <input
                type="checkbox"
                onChange={handleSelectAll}
                checked={selectedParcelas.length === parcelas.length && parcelas.length > 0}
              />
            </th>
            <th className="border border-gray-300 p-2 cursor-pointer" onClick={() => handleSort("id")}>ID</th>
            <th className="border border-gray-300 p-2 cursor-pointer" onClick={() => handleSort("nombre")}>Nombre</th>
            <th className="border border-gray-300 p-2 cursor-pointer" onClick={() => handleSort("cultivo")}>Cultivo</th>
            <th className="border border-gray-300 p-2 cursor-pointer" onClick={() => handleSort("area")}>Área</th>
          </tr>
        </thead>
        <tbody>
        {sortedParcelas.length > 0 ? (
            sortedParcelas.map((parcela) => (
              <tr key={`parcela-${parcela.id}`}>
                <td className="border border-gray-300 p-2 text-center">
                  <input type="checkbox" checked={selectedParcelas.includes(parcela.id)} onChange={() => setSelectedParcelas((prev) => (prev.includes(parcela.id) ? prev.filter((id) => id !== parcela.id) : [...prev, parcela.id]))} />
                </td>
                <td className="border border-gray-300 p-2 text-center">{parcela.id}</td>
                <td className="border border-gray-300 p-2">{parcela.nombre}</td>
                <td className="border border-gray-300 p-2 text-right">{parcela.cultivo}</td>
                <td className="border border-gray-300 p-2 text-right">{parcela.area}</td>

              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="border border-gray-300 p-4 text-center">No hay datos disponibles.</td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Botones de acción */}
      <div className="flex justify-start gap-4 mt-4">
        <button
          onClick={handleDeleteParcelas}
          disabled={selectedParcelas.length === 0}
          className={`p-2 rounded ${
            selectedParcelas.length > 0
              ? "bg-red-500 text-white hover:bg-red-600"
              : "bg-gray-300 text-gray-700 cursor-not-allowed"
          }`}
        >
          Eliminar Parcela(s)
        </button>
        <button
          onClick={handleEdit}
          disabled={selectedParcelas.length !== 1}
          className={`p-2 rounded ${
            selectedParcelas.length === 1
              ? "bg-blue-500 text-white hover:bg-blue-600"
              : "bg-gray-300 text-gray-700 cursor-not-allowed"
          }`}
        >
          Editar Parcela
        </button>
        <button
          onClick={handleDownloadCSV}
          disabled={selectedParcelas.length === 0}
          className={`p-2 rounded ${
            selectedParcelas.length > 0
              ? "bg-green-500 text-white hover:bg-green-600"
              : "bg-gray-300 text-gray-700 cursor-not-allowed"
          }`}
        >
          Descargar CSV
        </button>
      </div>

      {/* Formulario para crear una nueva parcela */}
      {showForm && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Nueva Parcela</h2>
            <div className="mb-4">
              <label className="block mb-1">id:</label>
              <input
                type="text"
                value={newParcela.id}
                onChange={(e) =>
                  setNewParcela((prev) => ({ ...prev, id: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Nombre:</label>
              <input
                type="text"
                value={newParcela.nombre}
                onChange={(e) =>
                  setNewParcela((prev) => ({ ...prev, nombre: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Geometria:</label>
              <input
                type="text"
                value={newParcela.geom ?? ""}
                onChange={(e) =>
                  setNewParcela((prev) => ({ ...prev, geom: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Cultivo:</label>
              <input
                type="text"
                value={newParcela.cultivo}
                onChange={(e) =>
                  setNewParcela((prev) => ({ ...prev, cultivo: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setShowForm(false)}
                className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
              >
                Cancelar
              </button>
              <button
                onClick={handleCreateParcela}
                className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
              >
                Crear
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Formulario para editar una parcela */}
            {editingParcela && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Editar Parcela</h2>
            <div className="mb-4">
              <label className="block mb-1">Nombre:</label>
              <input
                type="text"
                value={editingParcela.nombre}
                onChange={(e) =>
                  setEditingParcela((prev) => ({ ...prev, nombre: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Cultivo:</label>
              <input
                type="text"
                value={editingParcela.cultivo}
                onChange={(e) =>
                  setEditingParcela((prev) => ({ ...prev, cultivo: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">id:</label>
              <input
                type="text"
                value={editingParcela.id}
                onChange={(e) =>
                  setEditingParcela((prev) => ({ ...prev, id: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block mb-1">Geometria:</label>
              <input
                type="text"
                value={editingParcela.geom ?? ""}
                onChange={(e) =>
                  setEditingParcela((prev) => ({ ...prev, geom: e.target.value }))
                }
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setEditingParcela(null)}
                className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
              >
                Cancelar
              </button>
              <button
                onClick={handleUpdateParcela}
                className="bg-green-500 text-white p-2 rounded hover:bg-green-600"
              >
                Guardar cambios
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TableParcelas;