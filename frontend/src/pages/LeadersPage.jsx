import React from 'react';
import { motion } from 'framer-motion';
import DashboardLayout from '../components/DashboardLayout';
import LeaderDirectory from '../components/LeaderDirectory';

function LeadersPage() {
  return (
    <DashboardLayout title="Know Your Leaders" subtitle="Connect with your elected representatives.">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <LeaderDirectory />
      </motion.div>
    </DashboardLayout>
  );
}

export default LeadersPage;
