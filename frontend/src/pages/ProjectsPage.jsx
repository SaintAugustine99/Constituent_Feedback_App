import React from 'react';
import { motion } from 'framer-motion';
import DashboardLayout from '../components/DashboardLayout';
import ProjectTracker from '../components/ProjectTracker';

function ProjectsPage() {
  return (
    <DashboardLayout title="Project Tracker" subtitle="Track development projects in your area.">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <ProjectTracker />
      </motion.div>
    </DashboardLayout>
  );
}

export default ProjectsPage;
