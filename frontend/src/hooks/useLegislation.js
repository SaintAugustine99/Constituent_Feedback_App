import { useState, useEffect } from 'react';

// Replace with your actual Django URL
const API_BASE_URL = `${import.meta.env.VITE_API_URL}/legislation`;

/**
 * Custom Hook to fetch laws/bills
 * @param {string} endpoint - 'instruments', 'dockets', or 'feedback'
 * @param {object} filters - e.g. { search: 'finance', active: true }
 */
const useLegislation = (endpoint = 'instruments', filters = {}) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                // Build Query String (e.g. ?search=finance&docket=Nairobi)
                let queryParams = new URLSearchParams();
                Object.keys(filters).forEach(key => {
                    if (filters[key] !== undefined && filters[key] !== null && key !== 'activeOnly') {
                        queryParams.append(key, filters[key]);
                    }
                });

                // Handle the custom "active" endpoint
                let url = `${API_BASE_URL}/${endpoint}/`;
                if (filters.activeOnly) {
                    url = `${API_BASE_URL}/${endpoint}/active/`;
                }

                const response = await fetch(`${url}?${queryParams.toString()}`);

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                // Handle Django Pagination (DRF returns { count: ..., results: [...] })
                setData(result.results || result);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [endpoint, JSON.stringify(filters)]); // Re-run if filters change

    return { data, loading, error };
};

export default useLegislation;
