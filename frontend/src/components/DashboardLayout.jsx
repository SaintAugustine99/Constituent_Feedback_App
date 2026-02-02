import React, { useState, useContext } from 'react';
import styled from 'styled-components';
import { useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import NewsFeed from './NewsFeed';

// --- STYLED COMPONENTS (Jamii Olive Theme) ---

const DashboardContainer = styled.div`
  min-height: 100vh;
  background-color: ${({ theme }) => theme.colors.bg.primary};
  color: ${({ theme }) => theme.colors.text.primary};
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  font-family: ${({ theme }) => theme.fonts.body};

  @media (max-width: 1200px) {
    grid-template-columns: 280px 1fr;
  }

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const Sidebar = styled.aside`
  background-color: ${({ theme }) => theme.colors.bg.secondary};
  border-right: 1px solid ${({ theme }) => theme.colors.border};
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  transition: transform 0.3s ease-in-out;

  @media (max-width: 1024px) {
    position: fixed;
    top: 80px;
    left: 0;
    height: calc(100vh - 80px);
    width: 250px;
    z-index: 50;
    transform: ${({ isOpen }) => (isOpen ? 'translateX(0)' : 'translateX(-100%)')};
    box-shadow: ${({ isOpen }) => (isOpen ? '4px 0 10px rgba(0,0,0,0.1)' : 'none')};
    display: flex;
  }
`;

const MenuToggle = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: ${({ theme }) => theme.colors.brand.dark};
  cursor: pointer;
  margin-right: 1rem;

  @media (max-width: 1024px) {
    display: block;
  }
`;

const NewsToggle = styled.button`
  display: none;
  background: ${({ theme }) => theme.colors.brand.primary};
  color: white;
  border: none;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 100;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);

  @media (max-width: 1200px) {
    display: block;
  }
`;

const Overlay = styled.div`
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 40;

  @media (max-width: 1024px) {
    display: ${({ isOpen }) => (isOpen ? 'block' : 'none')};
  }
`;

const NewsFeedWrapper = styled.div`
  @media (max-width: 1200px) {
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 320px;
    z-index: 60;
    background: ${({ theme }) => theme.colors.bg.secondary};
    transform: ${({ isOpen }) => (isOpen ? 'translateX(0)' : 'translateX(100%)')};
    transition: transform 0.3s ease-in-out;
    overflow-y: auto;
    box-shadow: ${({ isOpen }) => (isOpen ? '-4px 0 10px rgba(0,0,0,0.1)' : 'none')};
  }
`;

const SidebarTitle = styled.h3`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 1.2rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid ${({ theme }) => theme.colors.accent.gold};
  padding-bottom: 0.5rem;
  display: inline-block;
`;

const NavItem = styled.div`
  padding: 0.8rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  color: ${({ theme, active }) => active ? 'white' : theme.colors.text.secondary};
  background: ${({ theme, active }) => active ? theme.colors.brand.primary : 'transparent'};
  font-weight: ${({ active }) => active ? '600' : '400'};
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${({ theme, active }) => active ? theme.colors.brand.primary : theme.colors.brand.washed};
    color: ${({ theme, active }) => active ? 'white' : theme.colors.brand.dark};
    transform: translateX(5px);
  }
`;

export const MainContent = styled.main`
  padding: 3rem;
  overflow-y: auto;

  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

export const HeaderSection = styled.div`
  margin-bottom: 3rem;
`;

export const PageTitle = styled.h1`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
`;

export const SubText = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  font-size: 1.1rem;
`;

function DashboardLayout({ children, title, subtitle }) {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [isNewsPanelOpen, setNewsPanelOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navTo = (path) => {
    navigate(path);
    setSidebarOpen(false);
  };

  return (
    <DashboardContainer>
      <Sidebar isOpen={isSidebarOpen}>
        <div>
          <SidebarTitle>Legislation</SidebarTitle>
          <NavItem active={isActive('/')} onClick={() => navTo('/')}>
            All Legislation
          </NavItem>
        </div>

        <div>
          <SidebarTitle>Actions</SidebarTitle>
          <NavItem active={isActive('/issues')} onClick={() => {
            if (!user) { alert("Login required."); return; }
            navTo('/issues');
          }}>
            Report an Issue
          </NavItem>
          <NavItem active={isActive('/facilities')} onClick={() => navTo('/facilities')}>
            Book Facilities
          </NavItem>
          <NavItem active={isActive('/projects')} onClick={() => navTo('/projects')}>
            Project Tracker
          </NavItem>
          <NavItem active={isActive('/leaders')} onClick={() => navTo('/leaders')}>
            Know Your Leaders
          </NavItem>
          <NavItem active={isActive('/news')} onClick={() => navTo('/news')}>
            News &amp; Resources
          </NavItem>
        </div>

        <div>
          <SidebarTitle>Your Space</SidebarTitle>
          <NavItem onClick={() => user ? console.log('Nav to Submissions') : alert('Please login to view your submissions.')}>
            My Submissions
          </NavItem>
          <NavItem onClick={() => user ? console.log('Nav to Saved') : alert('Please login to save bills.')}>
            Saved Bills
          </NavItem>
          <NavItem onClick={() => user ? console.log('Nav to Profile') : alert('Login to access profile settings.')}>
            Profile Settings
          </NavItem>
        </div>
      </Sidebar>

      <MainContent>
        <HeaderSection>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <MenuToggle onClick={() => setSidebarOpen(!isSidebarOpen)}>&#9776;</MenuToggle>
            <PageTitle>{title || 'Jamii Platform'}</PageTitle>
          </div>
          {subtitle && <SubText>{subtitle}</SubText>}
        </HeaderSection>
        {children}
      </MainContent>

      <Overlay isOpen={isSidebarOpen || isNewsPanelOpen} onClick={() => { setSidebarOpen(false); setNewsPanelOpen(false); }} />

      <NewsFeedWrapper isOpen={isNewsPanelOpen}>
        <NewsFeed />
      </NewsFeedWrapper>

      <NewsToggle onClick={() => setNewsPanelOpen(!isNewsPanelOpen)}>
        {isNewsPanelOpen ? 'Close' : 'News'}
      </NewsToggle>
    </DashboardContainer>
  );
}

export default DashboardLayout;
