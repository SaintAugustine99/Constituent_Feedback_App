import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { locationService, authService } from '../services/api';

// --- STYLES ---
const PageWrapper = styled.div`
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${({ theme }) => theme.colors.bg.primary};
  padding: 2rem 1rem;
  position: relative;
  z-index: 1;

  @media (max-width: 600px) {
    padding: 1rem;
    align-items: flex-start;
    padding-top: 2rem;
  }
`;

const FormCard = styled(motion.div)`
  background: ${({ theme }) => theme.colors.bg.surface};
  width: 100%;
  max-width: 500px;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  border-top: 5px solid ${({ theme }) => theme.colors.brand.primary};
`;

const Title = styled.h2`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  margin-bottom: 0.5rem;
  font-size: 2rem;
`;

const Subtitle = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  margin-bottom: 2rem;
`;

const InputGroup = styled.div`
  margin-bottom: 1.25rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: ${({ theme }) => theme.colors.brand.dark};
    font-weight: 600;
    font-size: 0.9rem;
  }
  
  input, select {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid ${({ theme }) => theme.colors.brand.light}40;
    border-radius: 8px;
    background: #ffffff; /* Force white background */
    color: #000000; /* Force black text */
    font-family: ${({ theme }) => theme.fonts.body};
    transition: all 0.2s;

    &:focus {
      outline: none;
      border-color: ${({ theme }) => theme.colors.brand.primary};
      background: #ffffff;
    }
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 1rem;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: transform 0.2s;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.dark};
    transform: translateY(-2px);
  }
  
  &:disabled {
    background: ${({ theme }) => theme.colors.text.secondary};
    cursor: not-allowed;
  }
`;

const ErrorMsg = styled.div`
  background: #ffebee;
  color: #c62828;
  padding: 0.8rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
`;

// --- COMPONENT ---
const Register = () => {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        ward_id: ''
    });

    // Location Data State
    const [counties, setCounties] = useState([]);
    const [constituencies, setConstituencies] = useState([]);
    const [wards, setWards] = useState([]);

    // Selection Logic
    const [selectedCounty, setSelectedCounty] = useState('');
    const [selectedConstituency, setSelectedConstituency] = useState('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Load Counties on Mount
    useEffect(() => {
        locationService.getCounties()
            .then(data => {
                console.log("Counties loaded:", data);
                // Handle optional pagination if backend introduces it unexpectedly
                const list = Array.isArray(data) ? data : (data.results || []);
                setCounties(list);
            })
            .catch(err => {
                console.error("Failed to load counties", err);
                setError("Failed to load location data. Please refresh.");
            });
    }, []);

    // Handle County Change
    const handleCountyChange = async (e) => {
        const countyId = e.target.value;
        setSelectedCounty(countyId);
        setSelectedConstituency('');
        setWards([]);
        setFormData({ ...formData, ward_id: '' });

        if (countyId) {
            const data = await locationService.getConstituencies(countyId);
            setConstituencies(data);
        }
    };

    // Handle Constituency Change
    const handleConstituencyChange = async (e) => {
        const constId = e.target.value;
        setSelectedConstituency(constId);
        setFormData({ ...formData, ward_id: '' });

        if (constId) {
            const data = await locationService.getWards(constId);
            setWards(data);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await authService.register(formData);
            navigate('/login');
        } catch (err) {
            setError("Registration failed. Please check your details.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageWrapper>
            <FormCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                <Title>Join Jamii.</Title>
                <Subtitle>Connect with your local governance.</Subtitle>

                {error && <ErrorMsg>{error}</ErrorMsg>}

                <form onSubmit={handleSubmit}>
                    <InputGroup>
                        <label>Username</label>
                        <input
                            type="text" required placeholder="e.g. CitizenJane"
                            value={formData.username}
                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        />
                    </InputGroup>

                    <InputGroup>
                        <label>Email</label>
                        <input
                            type="email" required placeholder="jane@example.com"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        />
                    </InputGroup>

                    <InputGroup>
                        <label>Password</label>
                        <input
                            type="password" required
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        />
                    </InputGroup>

                    <hr style={{ margin: '2rem 0', opacity: 0.1 }} />

                    <InputGroup>
                        <label>County</label>
                        <select value={selectedCounty} onChange={handleCountyChange} required>
                            <option value="">Select County... ({counties.length} available)</option>
                            {counties.map(c => (
                                <option key={c.id} value={c.id}>{c.name}</option>
                            ))}
                        </select>
                    </InputGroup>

                    <InputGroup>
                        <label>Constituency</label>
                        <select
                            value={selectedConstituency} onChange={handleConstituencyChange}
                            disabled={!selectedCounty} required
                        >
                            <option value="">Select Constituency...</option>
                            {constituencies.map(c => (
                                <option key={c.id} value={c.id}>{c.name}</option>
                            ))}
                        </select>
                    </InputGroup>

                    <InputGroup>
                        <label>Ward (Your Local Area)</label>
                        <select
                            value={formData.ward_id}
                            onChange={(e) => setFormData({ ...formData, ward_id: e.target.value })}
                            disabled={!selectedConstituency} required
                        >
                            <option value="">Select Ward...</option>
                            {wards.map(w => (
                                <option key={w.id} value={w.id}>{w.name}</option>
                            ))}
                        </select>
                    </InputGroup>

                    <Button type="submit" disabled={loading}>
                        {loading ? 'Registering...' : 'Create Account'}
                    </Button>
                </form>
            </FormCard>
        </PageWrapper>
    );
};

export default Register;
