import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { newsService } from '../services/api';

const FeedContainer = styled.div`
  background-color: ${({ theme }) => theme.colors.bg.secondary};
  border-left: 1px solid ${({ theme }) => theme.colors.border};
  padding: 1.5rem;
  height: 100vh;
  overflow-y: auto;
  font-family: ${({ theme }) => theme.fonts.body};

  @media (max-width: 1200px) {
    display: none;
  }
`;

const FeedHeader = styled.h3`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid ${({ theme }) => theme.colors.accent.gold};
  display: inline-block;
  padding-bottom: 0.2rem;
`;

const NewsItem = styled(motion.div)`
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

const SourceRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
  font-size: 0.75rem;
  color: ${({ theme }) => theme.colors.text.secondary};
`;

const SourceTag = styled.span`
  font-weight: 700;
  text-transform: uppercase;
  color: ${({ theme }) => theme.colors.brand.primary};
`;

const Headline = styled.a`
  font-size: 0.95rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.text.primary};
  line-height: 1.4;
  margin-bottom: 0.5rem;
  cursor: pointer;
  display: block;
  text-decoration: none;

  &:hover {
    color: ${({ theme }) => theme.colors.brand.primary};
    text-decoration: underline;
  }
`;

const ViewAllLink = styled.button`
  display: block;
  width: 100%;
  margin-top: 1.5rem;
  padding: 0.7rem;
  background: ${({ theme }) => theme.colors.brand.washed};
  color: ${({ theme }) => theme.colors.brand.dark};
  border: 1px solid ${({ theme }) => theme.colors.brand.primary};
  border-radius: ${({ theme }) => theme.borderRadius};
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  text-align: center;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.primary};
    color: white;
  }
`;

const LoadingText = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  font-size: 0.85rem;
  text-align: center;
  padding: 2rem 0;
`;

// Fallback mock data shown when API is unavailable
const FALLBACK_NEWS = [
  { id: 'f1', source_name: 'The Star', time_ago: '2h ago', title: 'Nairobi County Assembly debates new Zoning Policy for residential areas.', url: '#' },
  { id: 'f2', source_name: 'Senate Watch', time_ago: '4h ago', title: 'Senate Committee on Health to visit KNH following outcry over equipment.', url: '#' },
  { id: 'f3', source_name: 'County Gazette', time_ago: '6h ago', title: 'Notice of Public Participation: Finance Bill 2026 hearings start Monday.', url: '#' },
  { id: 'f4', source_name: 'Transport Authority', time_ago: '1d ago', title: 'New Matatu Terminus planned for Green Park to deconstruct traffic.', url: '#' },
  { id: 'f5', source_name: 'Education Ministry', time_ago: '1d ago', title: 'Vocational Training Centers to receive increased capitation grants.', url: '#' },
];

const NewsFeed = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    newsService.getArticles()
      .then((data) => {
        const results = data.results || data;
        setArticles(results.length > 0 ? results.slice(0, 8) : FALLBACK_NEWS);
      })
      .catch(() => {
        setArticles(FALLBACK_NEWS);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <FeedContainer>
      <FeedHeader>Civic Updates</FeedHeader>

      {loading ? (
        <LoadingText>Loading headlines...</LoadingText>
      ) : (
        articles.map((item, index) => (
          <NewsItem
            key={item.id}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <SourceRow>
              <SourceTag>{item.source_name}</SourceTag>
              <span>{item.time_ago}</span>
            </SourceRow>
            <Headline href={item.url} target="_blank" rel="noopener noreferrer">
              {item.title}
            </Headline>
          </NewsItem>
        ))
      )}

      <ViewAllLink onClick={() => navigate('/news')}>
        View All News &amp; Resources
      </ViewAllLink>

      <div style={{ marginTop: '1rem', padding: '1rem', background: '#fff3cd', borderRadius: '8px', fontSize: '0.8rem', color: '#856404' }}>
        <strong>Did you know?</strong> You can subscribe to specific dockets to get SMS alerts.
      </div>
    </FeedContainer>
  );
};

export default NewsFeed;
