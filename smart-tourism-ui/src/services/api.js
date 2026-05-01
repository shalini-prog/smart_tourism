import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getAllLocations = () => API.get("/predict_all");

export const getAdvisory = (id) =>
  API.get(`/smart_advisory/${id}`);