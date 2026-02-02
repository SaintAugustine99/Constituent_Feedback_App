import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import DashboardLayout, { MainContent, HeaderSection, PageTitle, SubText } from '../components/DashboardLayout';
import { newsService } from '../services/api';

// --- Styled Components ---

const SectionTitle = styled.h2`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid ${({ theme }) => theme.colors.accent.gold};
  padding-bottom: 0.5rem;
  display: inline-block;
`;

const ArticlesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
`;

const ArticleCard = styled(motion.a)`
  background: ${({ theme }) => theme.colors.bg.secondary};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: ${({ theme }) => theme.colors.brand.primary};
  }
`;

const ArticleImage = styled.div`
  width: 100%;
  height: 160px;
  background: ${({ theme }) => theme.colors.brand.washed};
  background-image: ${({ src }) => (src ? `url(${src})` : 'none')};
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: ${({ theme }) => theme.colors.brand.primary};
`;

const ArticleBody = styled.div`
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const ArticleSource = styled.span`
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: ${({ theme }) => theme.colors.brand.primary};
  margin-bottom: 0.3rem;
`;

const ArticleTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.text.primary};
  line-height: 1.4;
  margin-bottom: 0.5rem;
  flex: 1;
`;

const ArticleMeta = styled.span`
  font-size: 0.75rem;
  color: ${({ theme }) => theme.colors.text.secondary};
`;

const CategoryGroup = styled.div`
  margin-bottom: 2rem;
`;

const CategoryLabel = styled.h3`
  font-family: ${({ theme }) => theme.fonts.heading};
  color: ${({ theme }) => theme.colors.brand.dark};
  font-size: 1.1rem;
  margin-bottom: 1rem;
`;

const ResourceList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
`;

const ResourceCard = styled.a`
  display: block;
  background: ${({ theme }) => theme.colors.bg.secondary};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: 1rem 1.2rem;
  text-decoration: none;
  color: inherit;

  &:hover {
    border-color: ${({ theme }) => theme.colors.brand.primary};
    background: ${({ theme }) => theme.colors.brand.washed};
  }
`;

const ResourceName = styled.h4`
  font-size: 0.95rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.brand.dark};
  margin-bottom: 0.3rem;
`;

const ResourceDesc = styled.p`
  font-size: 0.8rem;
  color: ${({ theme }) => theme.colors.text.secondary};
  line-height: 1.4;
  margin: 0;
`;

const LoadingText = styled.p`
  color: ${({ theme }) => theme.colors.text.secondary};
  font-size: 0.9rem;
  padding: 2rem 0;
`;

// --- Component ---

function NewsResourcesPage() {
  const [articles, setArticles] = useState([]);
  const [resources, setResources] = useState([]);
  const [loadingArticles, setLoadingArticles] = useState(true);
  const [loadingResources, setLoadingResources] = useState(true);

  useEffect(() => {
    newsService.getArticles()
      .then((data) => setArticles(data.results || data))
      .catch(() => setArticles([]))
      .finally(() => setLoadingArticles(false));

    newsService.getResources()
      .then((data) => setResources(data.results || data))
      .catch(() => setResources([]))
      .finally(() => setLoadingResources(false));
  }, []);

  // Group resources by category_display
  const grouped = resources.reduce((acc, r) => {
    const key = r.category_display || r.category;
    if (!acc[key]) acc[key] = [];
    acc[key].push(r);
    return acc;
  }, {});

  return (
    <DashboardLayout title="News & Resources" subtitle="Stay informed with the latest civic headlines and government resources">
      {/* News Articles Section */}
      <SectionTitle>Latest Headlines</SectionTitle>

      {loadingArticles ? (
        <LoadingText>Loading articles...</LoadingText>
      ) : articles.length === 0 ? (
        <LoadingText>No articles available. Run the fetch_news management command to populate headlines.</LoadingText>
      ) : (
        <ArticlesGrid>
          {articles.map((article, index) => (
            <ArticleCard
              key={article.id}
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <ArticleImage src={article.image_url}>
                {!article.image_url && '📰'}
              </ArticleImage>
              <ArticleBody>
                <ArticleSource>{article.source_name}</ArticleSource>
                <ArticleTitle>{article.title}</ArticleTitle>
                {article.description && (
                  <ArticleMeta style={{ marginBottom: '0.5rem', fontSize: '0.82rem' }}>
                    {article.description.slice(0, 120)}
                    {article.description.length > 120 ? '...' : ''}
                  </ArticleMeta>
                )}
                <ArticleMeta>{article.time_ago}</ArticleMeta>
              </ArticleBody>
            </ArticleCard>
          ))}
        </ArticlesGrid>
      )}

      {/* Government Resources Section */}
      <SectionTitle>Government Resources</SectionTitle>

      {loadingResources ? (
        <LoadingText>Loading resources...</LoadingText>
      ) : Object.keys(grouped).length === 0 ? (
        <LoadingText>No resources available. Run the seed_resources management command to populate links.</LoadingText>
      ) : (
        Object.entries(grouped).map(([category, items]) => (
          <CategoryGroup key={category}>
            <CategoryLabel>{category}</CategoryLabel>
            <ResourceList>
              {items.map((resource) => (
                <ResourceCard
                  key={resource.id}
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ResourceName>{resource.name}</ResourceName>
                  <ResourceDesc>{resource.description}</ResourceDesc>
                </ResourceCard>
              ))}
            </ResourceList>
          </CategoryGroup>
        ))
      )}
    </DashboardLayout>
  );
}

export default NewsResourcesPage;
