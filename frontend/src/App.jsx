import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GlobalStyles } from './styles/GlobalStyles';
import { lightTheme, darkTheme } from './styles/theme';
import { AuthProvider } from './context/AuthContext'; // <--- Import Provider

// Components
import Header from './components/Header';
import Register from './pages/Register';
import Login from './pages/Login'; // <--- Import Login

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <AuthProvider> {/* <--- Wrap the whole app */}
      <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
        <GlobalStyles />
        <Router>
          <Header 
            isDarkMode={isDarkMode} 
            toggleTheme={() => setIsDarkMode(!isDarkMode)} 
          />
          
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} /> {/* <--- Route Added */}
            <Route path="/" element={
              <div style={{padding:'5rem', textAlign:'center'}}>
                <h1>Dashboard</h1>
                <p>Authentication flow is now complete.</p>
              </div>
            } />
          </Routes>
          
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
