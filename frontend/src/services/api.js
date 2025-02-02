import axios from 'axios';

// Base URL del backend
const API = axios.create({
  baseURL: "http://localhost:8000/api/v1", // Cambia según la configuración de tu backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getParcelas = async () => {
  const response = await API.get('/parcelas');
  return response.data;
};

export const updateParcela = async (id, data) => {
  const response = await API.put(`/parcelas/${id}`, data);
  return response.data;
};

export const createParcela = async (parcela) => {
  try {
    // Usamos API.post para que utilice el baseURL configurado
    const response = await API.post("/parcelas", parcela);
    return response.data;
  } catch (error) {
    console.error("Error en la solicitud:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteParcela = async (id) => {
  const response = await API.delete(`/parcelas/${id}`);
  return response.data;
};

export default API;
