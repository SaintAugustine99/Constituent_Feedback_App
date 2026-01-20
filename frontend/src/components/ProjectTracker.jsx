import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { projectService } from '../services/api';

const List = styled.div`
  display: flex; flex-direction: column; gap: 1rem;
`;

const ProjectCard = styled.div`
  background: white; padding: 1.5rem; border-radius: 8px; border-left: 5px solid ${props => props.status === 'ONGOING' ? '#F7C600' : '#4CAF50'};
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
`;

const StatusBadge = styled.span`
  background: #eee; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold;
`;

const ProjectTracker = () => {
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        projectService.getAll().then(setProjects).catch(console.error);
    }, []);

    return (
        <div style={{ padding: '2rem' }}>
            <h2>Development Tracker</h2>
            <p>Monitor CDF and County projects in your Ward.</p>
            <br />
            <List>
                {projects.map(p => (
                    <ProjectCard key={p.id} status={p.status}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <h3>{p.name}</h3>
                            <StatusBadge>{p.status}</StatusBadge>
                        </div>
                        <p>{p.description}</p>
                        <p><strong>Contractor:</strong> {p.contractor_name || 'N/A'}</p>
                        <p><strong>Budget:</strong> KES {Number(p.budget_allocated).toLocaleString()}</p>
                        <div style={{ marginTop: '1rem', background: '#f0f0f0', height: '10px', borderRadius: '5px' }}>
                            <div style={{ width: `${p.completion_percentage}%`, background: '#2E4F2F', height: '100%', borderRadius: '5px' }}></div>
                        </div>
                        <small>{p.completion_percentage}% Complete</small>
                    </ProjectCard>
                ))}
            </List>
            {projects.length === 0 && <p>No projects visible for your location.</p>}
        </div>
    );
};

export default ProjectTracker;
