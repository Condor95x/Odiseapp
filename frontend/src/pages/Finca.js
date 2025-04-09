import React,{ useState }  from 'react';
import TableOperaciones from '../components/TableOperaciones';

const Finca = () => {
  const [showOperaciones, setShowOperaciones] = useState(true);
  const Spacer = ({ width }) => <div style={{ width: `${width}rem`, display: 'inline-block' }}></div>;

  const handleShowOperaciones = () => {
    setShowOperaciones(!showOperaciones);
  };
  return (
    <div className="Contenedor">
      <div className="titulo-seccion">
        <h1>Mis fincas</h1>
        <button
          onClick={handleShowOperaciones}
          className={showOperaciones ? 'btn btn-secondary' : 'btn btn-primary'}
          >
          {showOperaciones ? 'Ocultar Operaciones' : 'Mostrar Operaciones'}
        </button>
        <Spacer width={0.1} />
      </div>
      {showOperaciones && (
      <div>
        <div className="titulo-seccion">
        <h2>Mis Operaciones</h2>
        </div>  
        <TableOperaciones />
    </div>
    )}
    </div>
  );
}

export default Finca; 