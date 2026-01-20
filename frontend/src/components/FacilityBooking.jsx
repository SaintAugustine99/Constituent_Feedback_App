import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { facilityService } from '../services/api';

const Container = styled.div`
  padding: 2rem;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const Card = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  border: 1px solid #eee;
  
  h3 { margin-bottom: 0.5rem; color: #2E4F2F; }
  p { color: #666; font-size: 0.9rem; margin-bottom: 1rem; }
`;

const Button = styled.button`
  background: #2E4F2F;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  
  &:hover { background: #1a301b; }
`;

const ModalOverlay = styled.div`
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white; padding: 2rem; borderRadius: 12px; width: 400px;
  input, select { width: 100%; padding: 0.8rem; margin: 0.5rem 0; border: 1px solid #ddd; }
`;

const FacilityBooking = () => {
    const [facilities, setFacilities] = useState([]);
    const [selectedFacility, setSelectedFacility] = useState(null);
    const [bookingData, setBookingData] = useState({ start_time: '', end_time: '', purpose: '' });
    const [message, setMessage] = useState('');

    useEffect(() => {
        facilityService.getAll().then(setFacilities).catch(console.error);
    }, []);

    const handleBook = async (e) => {
        e.preventDefault();
        try {
            await facilityService.book({
                facility: selectedFacility.id,
                ...bookingData
            });
            setMessage('Booking requested successfully!');
            setTimeout(() => { setSelectedFacility(null); setMessage(''); }, 2000);
        } catch (err) {
            setMessage('Booking failed. Time slot might be taken.');
        }
    };

    return (
        <Container>
            <h2>Public Assets</h2>
            <p>Book local halls, fields, and parks managed by the county.</p>
            <br />
            <Grid>
                {facilities.map(f => (
                    <Card key={f.id}>
                        <h3>{f.name}</h3>
                        <p>{f.type_display} • Cap: {f.capacity}</p>
                        <p>{f.ward_name}</p>
                        <Button onClick={() => setSelectedFacility(f)}>Book Now</Button>
                    </Card>
                ))}
            </Grid>
            {facilities.length === 0 && <p>No facilities found.</p>}

            {selectedFacility && (
                <ModalOverlay onClick={() => setSelectedFacility(null)}>
                    <ModalContent onClick={e => e.stopPropagation()}>
                        <h3>Book {selectedFacility.name}</h3>
                        {message && <p style={{ color: message.includes('success') ? 'green' : 'red' }}>{message}</p>}
                        <form onSubmit={handleBook}>
                            <label>Start Time</label>
                            <input type="datetime-local" required onChange={e => setBookingData({ ...bookingData, start_time: e.target.value })} />
                            <label>End Time</label>
                            <input type="datetime-local" required onChange={e => setBookingData({ ...bookingData, end_time: e.target.value })} />
                            <label>Purpose</label>
                            <input type="text" placeholder="e.g. Community Meeting" required onChange={e => setBookingData({ ...bookingData, purpose: e.target.value })} />
                            <Button type="submit">Confirm Booking</Button>
                        </form>
                    </ModalContent>
                </ModalOverlay>
            )}
        </Container>
    );
};

export default FacilityBooking;
