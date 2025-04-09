import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';

// Componente para rutas que requieren autenticación
export const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  // Mientras se verifica la autenticación, mostrar un spinner o similar
  if (loading) {
    return <div className="loading">Cargando...</div>;
  }
  
  // Si no hay usuario autenticado, redirigir al login
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  // Si hay usuario, mostrar el contenido
  return children;
};

// Componente para rutas que requieren un rol específico
export const RoleBasedRoute = ({ requiredRole, children }) => {
  const { user, loading, hasRole } = useAuth();
  
  if (loading) {
    return <div className="loading">Cargando...</div>;
  }
  
  // Si no hay usuario autenticado, redirigir al login
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  // Si el usuario no tiene el rol requerido, redirigir a la página principal
  if (!hasRole(requiredRole)) {
    return <Navigate to="/" />;
  }
  
  // Si el usuario tiene el rol adecuado, mostrar el contenido
  return children;
};

// Componente para rutas que requieren acceso a un módulo específico
export const ModuleBasedRoute = ({ module, children }) => {
  const { user, loading, hasModuleAccess } = useAuth();
  
  if (loading) {
    return <div className="loading">Cargando...</div>;
  }
  
  // Si no hay usuario autenticado, redirigir al login
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  // Si el usuario no tiene acceso al módulo, redirigir a la página principal
  if (!hasModuleAccess(module)) {
    return <Navigate to="/" />;
  }
  
  // Si el usuario tiene acceso al módulo, mostrar el contenido
  return children;
};