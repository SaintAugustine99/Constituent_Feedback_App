import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GlobalStyles } from './styles/GlobalStyles';
import { lightTheme, darkTheme } from './styles/theme';
import { AuthProvider } from './context/AuthContext';
import { AssistantProvider } from './context/AssistantContext';

// Components
import Header from './components/Header';
import ErrorBoundary from './components/ErrorBoundary';
import ChatWidget from './components/ChatWidget';

// Pages
import Register from './pages/Register';
import Login from './pages/Login';
import LegislationPage from './pages/LegislationPage';
import IssuesPage from './pages/IssuesPage';
import FacilitiesPage from './pages/FacilitiesPage';
import ProjectsPage from './pages/ProjectsPage';
import LeadersPage from './pages/LeadersPage';
import Community from './pages/Community';
import NewsResourcesPage from './pages/NewsResourcesPage';
import AssistantPage from './pages/AssistantPage';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <AuthProvider>
      <AssistantProvider>
        <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
          <GlobalStyles />
          <Router>
            <Header
              isDarkMode={isDarkMode}
              toggleTheme={() => setIsDarkMode(!isDarkMode)}
            />

            <ErrorBoundary>
              <Routes>
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<LegislationPage />} />
                <Route path="/issues" element={<IssuesPage />} />
                <Route path="/facilities" element={<FacilitiesPage />} />
                <Route path="/projects" element={<ProjectsPage />} />
                <Route path="/leaders" element={<LeadersPage />} />
                <Route path="/community" element={<Community />} />
                <Route path="/news" element={<NewsResourcesPage />} />
                <Route path="/assistant" element={<AssistantPage />} />
              </Routes>
            </ErrorBoundary>

            <ChatWidget />
          </Router>
        </ThemeProvider>
      </AssistantProvider>
    </AuthProvider>
  );
}

export default App;
