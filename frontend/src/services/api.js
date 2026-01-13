import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api';

export const getRaces = async () => {
    const response = await axios.get(`${API_BASE_URL}/races`);
    return response.data;
};

export const getDriverStandings = async (raceId) => {
    const response = await axios.get(`${API_BASE_URL}/standings/drivers`, {
        params: { upToRaceId: raceId }
    });
    return response.data;
};

export const getConstructorStandings = async (raceId) => {
    const response = await axios.get(`${API_BASE_URL}/standings/constructors`, {
        params: { upToRaceId: raceId }
    });
    return response.data;
};