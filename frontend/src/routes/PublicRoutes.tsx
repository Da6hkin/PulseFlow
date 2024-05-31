import React from 'react'
import { Route, Routes } from 'react-router-dom'
import SignInPage from 'src/pages/SignInPage'

const PublicRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<SignInPage />} />
      <Route path="*" element={<SignInPage />} />
    </Routes>
  )
}

export default PublicRoutes
