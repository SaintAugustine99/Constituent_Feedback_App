import React from 'react';
import { motion } from 'framer-motion';
import DashboardLayout from '../components/DashboardLayout';
import IssueReporter from '../components/IssueReporter';

function IssuesPage() {
  return (
    <DashboardLayout title="Report an Issue" subtitle="Report infrastructure or service issues in your area.">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <IssueReporter onSuccess={() => console.log("Issue Reported")} />
      </motion.div>
    </DashboardLayout>
  );
}

export default IssuesPage;
