import React, { useState } from 'react';
import TableWineryTask from '../components/TableTaskWinery';
import VesselManagement from '../components/VesselManagement';
import BatchManagement from '../components/BatchManagement';

function Bodega() {
  const [showVessels, setShowVessels] = useState(false);
  const [showActivities, setShowActivities] = useState(true);
  const [showBatch, setShowBatch] = useState(false);
  const Spacer = ({ width }) => <div style={{ width: `${width}rem`, display: 'inline-block' }}></div>;

  const handleShowVessels = () => {
    setShowVessels(!showVessels);
  };

  const handleShowActivities = () => {
    setShowActivities(!showActivities);
  };

  const handleShowBatch = () => {
    setShowBatch(!showBatch);
  };

  return (
    <div className="Contenedor">
      <div className="titulo-seccion flex gap-20">
      <h1>Mi Bodega</h1>
        <button
          onClick={handleShowActivities}
          className={showActivities ? 'btn btn-secondary' : 'btn btn-primary'}
          >
          {showActivities ? 'Ocultar actividades' : 'Mostrar actividades'}
        </button>
        <Spacer width={0.5} />
        <button
          onClick={handleShowVessels}
          className={showVessels ? 'btn btn-secondary' : 'btn btn-primary'}
        >
          {showVessels ? 'Ocultar vasijas' : 'Gestión de vasijas'}
        </button>
        <Spacer width={0.5} />
        <button
          onClick={handleShowBatch}
          className={showBatch ? 'btn btn-secondary' : 'btn btn-primary'}
        >
          {showBatch ? 'Ocultar Lotes' : 'Gestión de Lotes'}
        </button>
      </div>
      {showActivities && (
        <div>
          <div className="titulo-seccion">
          <h2>Mis Actividades</h2>
          </div>
          <TableWineryTask />
        </div>
      )}
      {showVessels && (
        <div>
          <div className="titulo-seccion">
          <h2>Mis Vasijas</h2>
          </div>
          <VesselManagement />
        </div>
      )}
      {showBatch && (
        <div>
          <div className="titulo-seccion">
            <h2>Mis Lotes</h2>
          </div>
          <BatchManagement />
        </div>
      )}
    </div>
  );
}

export default Bodega;