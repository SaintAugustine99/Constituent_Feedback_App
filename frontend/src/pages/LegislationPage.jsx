import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import useLegislation from '../hooks/useLegislation';
import FeedbackForm from '../components/FeedbackForm';
import FeedbackStats from '../components/FeedbackStats';
import DashboardLayout from '../components/DashboardLayout';
import LoadingSpinner from '../components/LoadingSpinner';
import { useAssistant } from '../context/AssistantContext';

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

const SearchInput = styled.input`
  width: 100%;
  max-width: 400px;
  padding: 0.75rem 1rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  font-size: 1rem;
  margin-bottom: 1.5rem;
  background: ${({ theme }) => theme.colors.bg.surface};
  color: ${({ theme }) => theme.colors.text.primary};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.brand.primary};
    box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.brand.washed};
  }
`;

function LegislationPage() {
  const { data: instruments, loading } = useLegislation('instruments', { activeOnly: true });
  const [selectedInstrument, setSelectedInstrument] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { setActiveInstrumentId } = useAssistant();

  const selectInstrument = (item) => {
    setSelectedInstrument(item);
    setActiveInstrumentId(item ? item.id : null);
  };

  const filteredInstruments = searchQuery
    ? instruments.filter(i =>
        i.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        i.docket_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (i.category_name && i.category_name.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : instruments;

  return (
    <DashboardLayout title="Legislative Tracker" subtitle="Participate in the decisions shaping your future.">
      <AnimatePresence mode="wait">
        {!selectedInstrument ? (
          <motion.div
            key="list"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -10 }}
          >
            <SearchInput
              type="text"
              placeholder="Search legislation..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />

            <h3 style={{ marginBottom: '1.5rem', fontWeight: 'bold', color: '#556B2F' }}>
              Active Opportunities
            </h3>

            {loading && <LoadingSpinner text="Loading legislation..." />}

            <CardsGrid>
              {filteredInstruments.map(item => (
                <InstrumentCard
                  key={item.id}
                  onClick={() => selectInstrument(item)}
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
                  No active legislation found.
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
            <BackButton onClick={() => selectInstrument(null)}>
              &larr; Back to List
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
                  Read Full Text
                </button>
              </div>

              <div style={{ marginTop: "3rem" }}>
                <FeedbackStats instrumentId={selectedInstrument.id} />
                <FeedbackForm
                  instrumentId={selectedInstrument.id}
                  instrumentTitle={selectedInstrument.title}
                />
              </div>
            </DetailPanel>
          </motion.div>
        )}
      </AnimatePresence>
    </DashboardLayout>
  );
}

export default LegislationPage;
