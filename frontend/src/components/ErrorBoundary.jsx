import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          padding: '2rem',
          textAlign: 'center',
          fontFamily: 'Inter, sans-serif',
        }}>
          <h2 style={{ color: '#c62828', marginBottom: '1rem' }}>Something went wrong</h2>
          <p style={{ color: '#666', marginBottom: '1.5rem', maxWidth: '400px' }}>
            An unexpected error occurred. Please try reloading the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              background: '#556B2F',
              color: 'white',
              border: 'none',
              padding: '0.75rem 2rem',
              borderRadius: '8px',
              fontSize: '1rem',
              cursor: 'pointer',
              fontWeight: 600,
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
