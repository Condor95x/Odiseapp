import React from 'react';
import Select from 'react-select'; // Asegúrate de importar Select

const MiFormulario = ({ newOperacion, setNewOperacion, usuarios, uniqueParcelas, options }) => {
  // ... (tus transformaciones de datos para react-select) ...

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}> {/* Contenedor principal con Grid */}
      <div> {/* Celda 1.1 */}
        <label className="modal-form-label">Operacion:</label>
        <Select
          options={options}
          onChange={(selectedOption) => setNewOperacion({ ...newOperacion, tipo_operacion: selectedOption.value })}
          value={options.find((option) => option.value === newOperacion.tipo_operacion)}
          placeholder="Selecciona una tarea"
          isSearchable
        />
      </div>
      <div> {/* Celda 1.2 */}
        <label className="modal-form-label">Parcela:</label>
        <Select
          options={parcelaOptions}
          onChange={(selectedOption) => setNewOperacion({ ...newOperacion, parcela_id: selectedOption.value })}
          value={parcelaOptions.find((option) => option.value === newOperacion.parcela_id)}
          placeholder="Selecciona una parcela"
          isSearchable
        />
      </div>

      <div> {/* Celda 2.1 */}
        <label className="modal-form-label">Responsable:</label>
        <Select
          options={responsableOptions}
          onChange={(selectedOption) => setNewOperacion({ ...newOperacion, responsable_id: selectedOption.value })}
          value={responsableOptions.find((option) => option.value === newOperacion.responsable_id)}
          placeholder="Selecciona un responsable"
          isSearchable
        />
      </div>
      <div> {/* Celda 2.2 */}
        <label className="modal-form-label">Estado:</label>
        <input
          type="text"
          value={newOperacion.estado}
          onChange={(e) => setNewOperacion({ ...newOperacion, estado: e.target.value })}
          className="modal-form-input"
        />
      </div>

      {/* ... (resto del formulario) ... */}
    </div>
  );
};

export default MiFormulario;