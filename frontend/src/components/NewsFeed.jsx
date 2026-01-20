import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const FeedContainer = styled.div`
  background-color: ${({ theme }) => theme.colors.bg.secondary};
  border-left: 1px solid ${({ theme }) => theme.colors.border};
  padding: 1.5rem;
  height: 100vh;
  overflow-y: auto;
  font-family: ${({ theme }) => theme.fonts.body};

  @media (max-width: 1200px) {
    display: none; /* Hide on smaller screens for now */
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

const Headline = styled.h4`
    font-size: 0.95rem;
    font-weight: 600;
    color: ${({ theme }) => theme.colors.text.primary};
    line-height: 1.4;
    margin-bottom: 0.5rem;
    cursor: pointer;

    &:hover {
        color: ${({ theme }) => theme.colors.brand.primary};
        text-decoration: underline;
    }
`;

const CategoryBadge = styled.span`
  background: ${({ theme }) => theme.colors.brand.washed};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 0.7rem;
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
`;

// Mock Data for Demo
const NEWS_DATA = [
    {
        id: 1,
        source: 'The Star',
        time: '2h ago',
        headline: 'Nairobi County Assembly debates new Zoning Policy for residential areas.',
        category: 'Urban Planning'
    },
    {
        id: 2,
        source: 'Senate Watch',
        time: '4h ago',
        headline: 'Senate Committee on Health to visit KNH following outcry over equipment.',
        category: 'Health'
    },
    {
        id: 3,
        source: 'County Gazette',
        time: '6h ago',
        headline: 'Notice of Public Participation: Finance Bill 2026 hearings start Monday.',
        category: 'Finance'
    },
    {
        id: 4,
        source: 'Transport Authority',
        time: '1d ago',
        headline: 'New Matatu Terminus planned for Green Park to deconstruct traffic.',
        category: 'Infrastructure'
    },
    {
        id: 5,
        source: 'Education Ministry',
        time: '1d ago',
        headline: 'Vocational Training Centers to receive increased capitation grants.',
        category: 'Education'
    }
];

const NewsFeed = () => {
    return (
        <FeedContainer>
            <FeedHeader>Civic Updates</FeedHeader>
            {NEWS_DATA.map((item, index) => (
                <NewsItem
                    key={item.id}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                >
                    <SourceRow>
                        <SourceTag>{item.source}</SourceTag>
                        <span>{item.time}</span>
                    </SourceRow>
                    <Headline>{item.headline}</Headline>
                    <CategoryBadge>{item.category}</CategoryBadge>
                </NewsItem>
            ))}

            <div style={{ marginTop: '2rem', padding: '1rem', background: '#fff3cd', borderRadius: '8px', fontSize: '0.8rem', color: '#856404' }}>
                <strong>Did you know?</strong> You can subscribe to specific dockets to get SMS alerts.
            </div>
        </FeedContainer>
    );
};

export default NewsFeed;
