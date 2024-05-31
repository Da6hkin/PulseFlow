import React from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from 'src/components/Layout'
import MiniLayout from 'src/components/MiniLayout'
import CompanyPage from 'src/pages/CompanyPage'
import FAQPage from 'src/pages/FAQPage'
import ProfilePage from 'src/pages/ProfilePage'
import ProjectPage from 'src/pages/ProjectPage'
import TaskPage from 'src/pages/TaskPage'
import TeamPage from 'src/pages/TeamPage'

const PrivateRoutes = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="*" element={<Navigate to="/profile" replace />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="company" element={<CompanyPage />} />
        <Route path="project" element={<ProjectPage />} />
        <Route path="faq" element={<FAQPage />} />
      </Route>
      <Route element={<MiniLayout />}>
        <Route path="team/:projectId/" element={<TeamPage />} />
        <Route path="task/:projectId/" element={<TaskPage />} />
      </Route>
    </Routes>
  )
}

export default PrivateRoutes
