import axios from 'axios';

export const serverUrl = `http://${process.env.REACT_APP_HOST}:8000`;

export const calculateExpression = async (expression) => {
	return axios.post(`${serverUrl}/calculate`, {
		expression: expression
	});
}

export const downloadAllCalculations = async () => {
	return axios.get(`${serverUrl}/calculations`, {
		responseType: 'blob'
	});
}