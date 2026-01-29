import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  to { transform: rotate(360deg); }
`;

const SpinnerWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
`;

const Spinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid ${({ theme }) => theme.colors.brand.washed};
  border-top-color: ${({ theme }) => theme.colors.brand.primary};
  border-radius: 50%;
  animation: ${spin} 0.8s linear infinite;
`;

const SpinnerText = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  font-size: 0.9rem;
`;

const LoadingSpinner = ({ text = 'Loading...' }) => (
  <SpinnerWrapper>
    <Spinner />
    <SpinnerText>{text}</SpinnerText>
  </SpinnerWrapper>
);

export default LoadingSpinner;
