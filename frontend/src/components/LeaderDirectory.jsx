import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { officialService } from '../services/api';

const Grid = styled.div`
  display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; padding: 2rem;
`;

const LeaderCard = styled.div`
  background: white; border-radius: 50vw 50vw 12px 12px; 
  text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  overflow: hidden;
`;

const Photo = styled.div`
  width: 100%; height: 250px; background: #ddd; 
  background-image: url(${props => props.src}); background-size: cover; background-position: center;
`;

const Info = styled.div`
  padding: 1.5rem;
  h3 { margin: 0; color: #2E4F2F; }
  span { color: #888; font-size: 0.9rem; display: block; margin-bottom: 1rem; }
`;

const ContactBtn = styled.a`
  display: inline-block; text-decoration: none;
  background: #25D366; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;
  &:hover { opacity: 0.9; }
`;

const LeaderDirectory = () => {
    const [officials, setOfficials] = useState([]);

    useEffect(() => {
        officialService.getAll().then(setOfficials).catch(console.error);
    }, []);

    return (
        <div>
            <h2 style={{ marginLeft: '2rem', marginTop: '1rem' }}>Know Your Leaders</h2>
            <Grid>
                {officials.map(leader => (
                    <LeaderCard key={leader.id}>
                        <Photo src={leader.photo || 'https://via.placeholder.com/250'} />
                        <Info>
                            <h3>{leader.name}</h3>
                            <span>{leader.title_display}</span>
                            {leader.whatsapp_link ? (
                                <ContactBtn href={leader.whatsapp_link} target="_blank">WhatsApp</ContactBtn>
                            ) : (
                                <p>No direct contact info.</p>
                            )}
                        </Info>
                    </LeaderCard>
                ))}
            </Grid>
            {officials.length === 0 && <p style={{ marginLeft: '2rem' }}>No officials found via directory.</p>}
        </div>
    );
};

export default LeaderDirectory;
