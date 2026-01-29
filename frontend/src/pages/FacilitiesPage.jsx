import React from 'react';
import { motion } from 'framer-motion';
import DashboardLayout from '../components/DashboardLayout';
import FacilityBooking from '../components/FacilityBooking';

function FacilitiesPage() {
  return (
    <DashboardLayout title="Book Facilities" subtitle="Reserve community spaces and facilities.">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <FacilityBooking />
      </motion.div>
    </DashboardLayout>
  );
}

export default FacilitiesPage;
