import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GlobalStyles } from './styles/GlobalStyles';
import { lightTheme, darkTheme } from './styles/theme';
import { AuthProvider } from './context/AuthContext';

// Components
import Header from './components/Header';
import Register from './pages/Register';
import Login from './pages/Login';
import LegislationDashboard from './pages/LegislationDashboard';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <AuthProvider>
      <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
        <GlobalStyles />
        <Router>
          <Header
            isDarkMode={isDarkMode}
            toggleTheme={() => setIsDarkMode(!isDarkMode)}
          />

          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<LegislationDashboard />} />
          </Routes>

        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
