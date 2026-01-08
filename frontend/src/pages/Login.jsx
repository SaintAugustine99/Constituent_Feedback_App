import React, { useState, useContext } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

// Reuse styles from Register for consistency
const PageWrapper = styled.div`
  min-height: calc(100vh - 80px); /* Account for header */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${({ theme }) => theme.colors.bg.primary};
  padding: 2rem 1rem;
  
  @media (max-width: 600px) {
    padding: 1rem;
  }
`;

const FormCard = styled(motion.div)`
  background: ${({ theme }) => theme.colors.bg.surface};
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  border-top: 5px solid ${({ theme }) => theme.colors.brand.primary};
`;

const Title = styled.h2`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
`;

const InputGroup = styled.div`
  margin-bottom: 1.5rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: ${({ theme }) => theme.colors.brand.dark};
    font-weight: 600;
  }
  
  input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid ${({ theme }) => theme.colors.brand.light}40;
    border-radius: 8px;
    background: ${({ theme }) => theme.colors.bg.primary};
    font-family: ${({ theme }) => theme.fonts.body};
    transition: all 0.2s;

    &:focus {
      outline: none;
      border-color: ${({ theme }) => theme.colors.brand.primary};
      background: white;
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
  transition: transform 0.2s;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.dark};
    transform: translateY(-2px);
  }
`;

const ErrorMsg = styled.div`
  background: #ffebee;
  color: #c62828;
  padding: 0.8rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
`;

const Login = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [formData, setFormData] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(formData);
      navigate('/');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageWrapper>
      <FormCard initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
        <Title>Welcome Back.</Title>
        {error && <ErrorMsg>{error}</ErrorMsg>}

        <form onSubmit={handleSubmit}>
          <InputGroup>
            <label>Username</label>
            <input
              type="text" required value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            />
          </InputGroup>

          <InputGroup>
            <label>Password</label>
            <input
              type="password" required value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </InputGroup>

          <Button type="submit" disabled={loading}>
            {loading ? 'Verifying...' : 'Login'}
          </Button>
        </form>

        <p style={{ marginTop: '1.5rem', textAlign: 'center', color: '#666' }}>
          New here? <Link to="/register" style={{ fontWeight: 'bold', color: '#556B2F' }}>Join Jamii</Link>
        </p>
      </FormCard>
    </PageWrapper>
  );
};

export default Login;
