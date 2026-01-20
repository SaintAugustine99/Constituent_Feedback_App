import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// --- STYLES (Reuse Theme) ---
// In a full app, these would be in a layout component
const PageContainer = styled.div`
  min-height: 100vh;
  background-color: ${({ theme }) => theme.colors.bg.primary};
  color: ${({ theme }) => theme.colors.text.primary};
  display: grid;
  grid-template-columns: 280px 1fr 300px; /* 3-Column like Dashboard */
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
  
  @media (max-width: 1024px) {
    display: none; // Mobile nav todo
  }
`;

const NavItem = styled.div`
  padding: 0.8rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: ${({ theme }) => theme.borderRadius};
  color: ${({ theme, active }) => active ? 'white' : theme.colors.text.secondary};
  background: ${({ theme, active }) => active ? theme.colors.brand.primary : 'transparent'};
  font-weight: ${({ active }) => active ? '600' : '400'};
  cursor: pointer;
  
  &:hover {
    background: ${({ theme, active }) => active ? theme.colors.brand.primary : theme.colors.brand.washed};
    color: ${({ theme, active }) => active ? 'white' : theme.colors.brand.dark};
  }
`;

const MainContent = styled.main`
  padding: 2rem;
  overflow-y: auto;
`;

const FeedColumn = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const TabBar = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  padding-bottom: 1rem;
`;

const Tab = styled.button`
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 700;
  color: ${({ theme, active }) => active ? theme.colors.brand.primary : theme.colors.text.secondary};
  border-bottom: 3px solid ${({ theme, active }) => active ? theme.colors.brand.primary : 'transparent'};
  padding-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    color: ${({ theme }) => theme.colors.brand.primary};
  }
`;

// --- POST COMPONENT ---
const PostCard = styled(motion.div)`
  background: ${({ theme }) => theme.colors.bg.surface};
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  border: 1px solid ${({ theme }) => theme.colors.border};
`;

const UserMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
`;

const Avatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${({ theme }) => theme.colors.brand.washed};
  color: ${({ theme }) => theme.colors.brand.dark};
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
`;

// --- AD COMPONENT ---
const SponsoredCard = styled(motion.div)`
  background: #fff8e1; /* Light yellow for visibility */
  border: 1px dashed #ffd54f;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
`;

const SponsoredLabel = styled.span`
  font-size: 0.7rem;
  font-weight: bold;
  color: #856404;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  display: block;
`;

// --- MOCK DATA ---
const POSTS = {
    national: [
        { id: 1, user: 'Maina K.', initial: 'M', ward: 'Nairobi', text: 'The Finance Bill 2026 seems to ignore the plight of small businesses. We need a clause for SMEs!', likes: 45, comments: 12 },
        { id: 2, user: 'Amina J.', initial: 'A', ward: 'Mombasa', text: 'Corruption in the Ministry of Health must be addressed before we approve any new budget allocations.', likes: 120, comments: 34 }
    ],
    county: [
        { id: 3, user: 'John Doe', initial: 'J', ward: 'Langata', text: 'Traffic on Langata Road is getting worse. The new zoning policy allows high-rises but no road expansion?', likes: 23, comments: 5 },
        { id: 4, user: 'Sarah O.', initial: 'S', ward: 'Westlands', text: 'Water rationing schedule is not being followed. We have been dry for 3 days.', likes: 12, comments: 2 }
    ],
    ward: [
        { id: 5, user: 'Mama Boi', initial: 'M', ward: 'Utawala', text: 'The streetlights near Utawala Complex are busted again. Secure our streets!', likes: 8, comments: 1 },
        { id: 6, user: 'Kevin M.', initial: 'K', ward: 'Utawala', text: 'Community clear-up this Saturday at the AP Camp. Who is joining?', likes: 15, comments: 6 }
    ]
};

// --- PAGE ---
const Community = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('national'); // national, county, ward

    return (
        <PageContainer>
            {/* SIDEBAR */}
            <Sidebar>
                <h3 style={{ fontFamily: 'Merriweather', color: '#404F24', fontSize: '1.2rem', marginBottom: '1rem' }}>Menu</h3>
                <NavItem onClick={() => navigate('/')}>Dashboard</NavItem>
                <NavItem active>Community Forum</NavItem>
                <NavItem>Petitions</NavItem>
            </Sidebar>

            {/* MAIN FEED */}
            <MainContent>
                <h1 style={{ fontFamily: 'Merriweather', color: '#404F24', marginBottom: '0.5rem' }}>Community Hub</h1>
                <p style={{ color: '#666', marginBottom: '2rem' }}>Connect with constituents in your area.</p>

                <FeedColumn>
                    <TabBar>
                        <Tab active={activeTab === 'national'} onClick={() => setActiveTab('national')}>Kenya (National)</Tab>
                        <Tab active={activeTab === 'county'} onClick={() => setActiveTab('county')}>My County (Nairobi)</Tab>
                        <Tab active={activeTab === 'ward'} onClick={() => setActiveTab('ward')}>My Ward (Utawala)</Tab>
                    </TabBar>

                    {/* AD SLOT 1 */}
                    <SponsoredCard initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <SponsoredLabel>Sponsored Partner</SponsoredLabel>
                        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                            <div style={{ width: 50, height: 50, background: '#eee', borderRadius: '4px' }}></div>
                            <div>
                                <h4 style={{ fontWeight: 'bold' }}>Civic Education Survey</h4>
                                <p style={{ fontSize: '0.9rem', color: '#555' }}>Participate in the Katiba Institute survey on Devolution.</p>
                            </div>
                        </div>
                    </SponsoredCard>

                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                        >
                            {POSTS[activeTab].map(post => (
                                <PostCard key={post.id}>
                                    <UserMeta>
                                        <Avatar>{post.initial}</Avatar>
                                        <div>
                                            <h4 style={{ fontSize: '0.95rem', fontWeight: 'bold' }}>{post.user}</h4>
                                            <span style={{ fontSize: '0.8rem', color: '#888' }}>{post.ward}</span>
                                        </div>
                                    </UserMeta>
                                    <p style={{ lineHeight: 1.6, color: '#333' }}>{post.text}</p>
                                    <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', fontSize: '0.85rem', color: '#666' }}>
                                        <span>❤️ {post.likes} Likes</span>
                                        <span>💬 {post.comments} Comments</span>
                                    </div>
                                </PostCard>
                            ))}
                        </motion.div>
                    </AnimatePresence>

                </FeedColumn>
            </MainContent>

            {/* RIGHT COLUMN (Ads/Trends) */}
            <div style={{ padding: '2rem', borderLeft: '1px solid rgba(85,107,47,0.2)' }}>
                <h4 style={{ fontWeight: 'bold', color: '#404F24', marginBottom: '1rem' }}>Trending Topics</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {['#FinanceBill2026', '#NairobiTraffic', '#DoctorsStrike', '#Devolution', '#UtawalaRoads'].map(tag => (
                        <span key={tag} style={{ background: '#E3E8D9', color: '#404F24', fontSize: '0.8rem', padding: '0.3rem 0.6rem', borderRadius: '20px' }}>{tag}</span>
                    ))}
                </div>

                <div style={{ marginTop: '3rem' }}>
                    <SponsoredLabel>Advertisement</SponsoredLabel>
                    <div style={{ height: '200px', background: '#e0e0e0', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#888' }}>
                        Google Ads / Local NGO Placeholders
                    </div>
                </div>
            </div>

        </PageContainer>
    );
};

export default Community;
