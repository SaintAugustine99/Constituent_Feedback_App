import React, { useState } from 'react';
import styled from 'styled-components';
import { issueService } from '../services/api';

const Container = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 0 auto;
`;

const Title = styled.h2`
  color: ${({ theme }) => theme.colors.brand.dark};
  margin-bottom: 1.5rem;
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
`;

const SubmitButton = styled.button`
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

const IssueReporter = ({ onSuccess }) => {
    const [formData, setFormData] = useState({
        category: 'ROAD',
        description: '',
        location_description: '',
        image_evidence: null
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        if (e.target.name === 'image_evidence') {
            setFormData({ ...formData, image_evidence: e.target.files[0] });
        } else {
            setFormData({ ...formData, [e.target.name]: e.target.value });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = new FormData();
            Object.keys(formData).forEach(key => {
                if (formData[key]) data.append(key, formData[key]);
            });

            await issueService.createRequest(data);
            setMessage('Issue reported successfully!');
            setFormData({ category: 'ROAD', description: '', location_description: '', image_evidence: null });
            if (onSuccess) onSuccess();
        } catch (error) {
            setMessage('Failed to report issue. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container>
            <Title>Report a Service Issue</Title>
            {message && <p style={{ color: message.includes('success') ? 'green' : 'red', marginBottom: '1rem' }}>{message}</p>}

            <form onSubmit={handleSubmit}>
                <FormGroup>
                    <label>Category</label>
                    <select name="category" value={formData.category} onChange={handleChange}>
                        <option value="ROAD">Roads & Transport</option>
                        <option value="WATER">Water & Sanitation</option>
                        <option value="POWER">Power & Lighting</option>
                        <option value="SECURITY">Security & Safety</option>
                        <option value="ENV">Environment & Garbage</option>
                        <option value="OTHER">Other</option>
                    </select>
                </FormGroup>

                <FormGroup>
                    <label>Description</label>
                    <textarea
                        name="description"
                        rows="4"
                        value={formData.description}
                        onChange={handleChange}
                        placeholder="Describe the issue in detail..."
                        required
                    />
                </FormGroup>

                <FormGroup>
                    <label>Location (Nearby Landmark)</label>
                    <input
                        type="text"
                        name="location_description"
                        value={formData.location_description}
                        onChange={handleChange}
                        placeholder="e.g. Near Main Market"
                    />
                </FormGroup>

                <FormGroup>
                    <label>Photo Evidence (Optional)</label>
                    <input type="file" name="image_evidence" accept="image/*" onChange={handleChange} />
                </FormGroup>

                <SubmitButton type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Report Issue'}
                </SubmitButton>
            </form>
        </Container>
    );
};

export default IssueReporter;
