import React, { useState, useContext } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import useLegislation from '../hooks/useLegislation';
import FeedbackForm from '../components/FeedbackForm';

import NewsFeed from '../components/NewsFeed';

// --- STYLED COMPONENTS (Jamii Olive Theme) ---

const DashboardContainer = styled.div`
  min-height: 100vh;
  background-color: ${({ theme }) => theme.colors.bg.primary};
  color: ${({ theme }) => theme.colors.text.primary};
  display: grid;
  grid-template-columns: 280px 1fr 320px; /* 3-Column Layout */
  font-family: ${({ theme }) => theme.fonts.body};

  @media (max-width: 1200px) {
    grid-template-columns: 280px 1fr; /* Hide news on medium screens */
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
    top: 80px; /* Assuming header height */
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

const MainContent = styled.main`
  padding: 3rem;
  overflow-y: auto;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const HeaderSection = styled.div`
  margin-bottom: 3rem;
`;

const PageTitle = styled.h1`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
`;

const SubText = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  font-size: 1.1rem;
`;

const CardsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
`;

const InstrumentCard = styled(motion.div)`
  background: ${({ theme }) => theme.colors.bg.surface};
  padding: 1.5rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  box-shadow: ${({ theme }) => theme.shadows.soft};
  border-left: 4px solid ${({ theme }) => theme.colors.brand.primary};
  cursor: pointer;
  position: relative;
  overflow: hidden;

  h3 {
    font-family: ${({ theme }) => theme.fonts.heading};
    font-size: 1.1rem;
    color: ${({ theme }) => theme.colors.text.primary};
    margin: 0.8rem 0;
    line-height: 1.4;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  }
`;

const Badge = styled.span`
  background: ${({ theme, type }) => type === 'deadline' ? '#ffebee' : theme.colors.brand.washed};
  color: ${({ theme, type }) => type === 'deadline' ? '#c62828' : theme.colors.brand.dark};
  padding: 0.25rem 0.8rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const DetailPanel = styled(motion.div)`
  position: relative;
  background: ${({ theme }) => theme.colors.bg.surface};
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0,0,0,0.1);
  margin-top: 2rem;
  border: 1px solid ${({ theme }) => theme.colors.border};

  h2 {
    font-family: ${({ theme }) => theme.fonts.heading};
    color: ${({ theme }) => theme.colors.brand.dark};
    font-size: 2rem;
    margin-bottom: 1rem;
  }
`;

const BackButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.colors.text.secondary};
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    color: ${({ theme }) => theme.colors.brand.primary};
  }
`;

// --- MAIN COMPONENT ---

function LegislationDashboard() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  // 1. Fetch Instruments Active
  const { data: instruments, loading, error } = useLegislation('instruments', { activeOnly: true });
  // 2. Fetch Dockets (Simulating fetch or using data)
  // In a real app we'd fetch this. Hardcoding for the "Crucial Dockets" demo request.
  const crucialDockets = [
    { id: 'all', name: 'All Legislation' },
    { id: 'dev', name: 'Devolution & Planning' },
    { id: 'infra', name: 'Infrastructure (Roads & Transport)' },
    { id: 'health', name: 'Health & Sanitation' },
    { id: 'edu', name: 'Education & Vocational Training' },
  ];

  // ... imports
  import IssueReporter from '../components/IssueReporter';
  import FacilityBooking from '../components/FacilityBooking';
  import ProjectTracker from '../components/ProjectTracker';
  import LeaderDirectory from '../components/LeaderDirectory';

  // ... (Sidebar styled component updates were already done)

  // ... inside LegislationDashboard function
  const [activeTab, setActiveTab] = useState('all');
  const [selectedInstrument, setSelectedInstrument] = useState(null);
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  // New State for View Mode ('legislation' or 'issues')
  const [viewMode, setViewMode] = useState('legislation'); // 'legislation', 'issues', 'facilities', 'projects', 'leaders'

  // ... filteredInstruments logic remains ...

  return (
    <DashboardContainer>
      <Sidebar isOpen={isSidebarOpen}>
        {/* ... Crucial Dockets ... */}
        <div>
          <SidebarTitle>Crucial Dockets</SidebarTitle>
          {crucialDockets.map(dock => (
            <NavItem
              key={dock.id}
              active={activeTab === dock.id && viewMode === 'legislation'}
              onClick={() => { setActiveTab(dock.id); setViewMode('legislation'); setSelectedInstrument(null); setSidebarOpen(false); }}
            >
              {dock.name}
            </NavItem>
          ))}
        </div>

        <div>
          <SidebarTitle>Actions</SidebarTitle>
          <NavItem
            active={viewMode === 'issues'}
            onClick={() => {
              if (!user) { alert("Login required."); return; }
              setViewMode('issues');
              setSidebarOpen(false);
            }}
          >
            🚧 Report an Issue
          </NavItem>
          <NavItem
            active={viewMode === 'facilities'}
            onClick={() => { setViewMode('facilities'); setSidebarOpen(false); }}
          >
            🏟 Book Facilities
          </NavItem>
          <NavItem
            active={viewMode === 'projects'}
            onClick={() => { setViewMode('projects'); setSidebarOpen(false); }}
          >
            🏗 Project Tracker
          </NavItem>
          <NavItem
            active={viewMode === 'leaders'}
            onClick={() => { setViewMode('leaders'); setSidebarOpen(false); }}
          >
            👔 Know Your Leaders
          </NavItem>
        </div>

        <div>
          {/* ... Your Space ... */}

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

      {/* MAIN CONTENT AREA */}
      <MainContent>
        <HeaderSection>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <MenuToggle onClick={() => setSidebarOpen(!isSidebarOpen)}>☰</MenuToggle>
            <PageTitle>Legislative Tracker</PageTitle>
          </div>
          <SubText>Participate in the decisions shaping your future.</SubText>
        </HeaderSection>

        {/* Render Views based on Mode */}
        {viewMode === 'issues' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <IssueReporter onSuccess={() => console.log("Issue Reported")} />
          </motion.div>
        )}

        {viewMode === 'facilities' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <FacilityBooking />
          </motion.div>
        )}

        {viewMode === 'projects' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <ProjectTracker />
          </motion.div>
        )}

        {viewMode === 'leaders' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <LeaderDirectory />
          </motion.div>
        )}

        {viewMode === 'legislation' && (
          <AnimatePresence mode="wait">
            {!selectedInstrument ? (
              <motion.div
                key="list"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -10 }}
              >
                {/* LIST VIEW */}
                <h3 style={{ marginBottom: '1.5rem', fontWeight: 'bold', color: '#556B2F' }}>
                  {activeTab === 'all' ? 'Active Opportunities' : `${crucialDockets.find(d => d.id === activeTab)?.name}`}
                </h3>

                {loading && <p>Loading legislation...</p>}

                <CardsGrid>
                  {filteredInstruments.map(item => (
                    <InstrumentCard
                      key={item.id}
                      onClick={() => setSelectedInstrument(item)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <Badge>{item.category_name}</Badge>
                      </div>
                      <h3>{item.title}</h3>
                      <p style={{ fontSize: '0.9rem', color: '#666' }}>{item.docket_name}</p>

                      <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #eee' }}>
                        <Badge type="deadline">
                          Due: {new Date(item.participation_deadline).toLocaleDateString()}
                        </Badge>
                      </div>
                    </InstrumentCard>
                  ))}

                  {instruments.length === 0 && !loading && (
                    <div style={{ gridColumn: '1 / -1', padding: '2rem', textAlign: 'center', background: 'white', borderRadius: '12px' }}>
                      No active legislation found for this category.
                    </div>
                  )}
                </CardsGrid>

              </motion.div>
            ) : (
              <motion.div
                key="detail"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                {/* DETAIL VIEW */}
                <BackButton onClick={() => setSelectedInstrument(null)}>
                  ← Back to List
                </BackButton>

                <DetailPanel>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div>
                      <Badge>{selectedInstrument.category_name}</Badge>
                      <h2>{selectedInstrument.title}</h2>
                      <p style={{ fontSize: "1.1rem", color: "#556B2F", fontWeight: "bold" }}>
                        {selectedInstrument.docket_name}
                      </p>
                    </div>
                    <Badge type="deadline">
                      Action Required by: {new Date(selectedInstrument.participation_deadline).toLocaleDateString()}
                    </Badge>
                  </div>

                  <div style={{ margin: "2rem 0", lineHeight: "1.8", color: "#444" }}>
                    <h4 style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>Executive Summary</h4>
                    <p>{selectedInstrument.summary_text || "No summary provided. Please refer to the full text."}</p>
                  </div>

                  <div style={{ display: "flex", gap: "1rem" }}>
                    <button style={{ padding: "0.8rem 1.5rem", background: "#f0f0f0", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" }}>
                      📄 Read Full Text
                    </button>
                  </div>

                  {/* FEEDBACK FORM INTEGRATION */}
                  <div style={{ marginTop: "3rem" }}>
                    <FeedbackForm
                      instrumentId={selectedInstrument.id}
                      instrumentTitle={selectedInstrument.title}
                    />
                  </div>

                </DetailPanel>
              </motion.div>
            )}
          </AnimatePresence>
        )}

      </MainContent>



      {/* RIGHT SIDEBAR (NEWS) */}
      <NewsFeed />
    </DashboardContainer >
  );
}

export default LegislationDashboard;
