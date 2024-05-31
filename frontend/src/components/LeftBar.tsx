import React from 'react'
import { Box, useTheme } from '@mui/material'
import LogoutIcon from '@mui/icons-material/Logout'
import { useLocation } from 'react-router-dom'
import LeftBarItem from './items/LeftBarItem'

const isMobile = window.innerWidth < 600

const items = ['ПРОФІЛЬ', 'КОМПАНІЇ', 'ПРОЕКТИ', 'FAQ']

const routerList = [
  '/profile',
  '/company',
  '/project',
  '/faq'
]

const LeftBar = () => {
  const theme = useTheme()
  const location = useLocation()

  const handleLogout = () => {
    localStorage.clear()
    window.location.reload()
  }

  return (
    <Box
      sx={{
        height: '100vh',
        backgroundColor: theme.palette.primary.light,
        padding: isMobile ? '5px 5px' : '50px 50px',
        boxShadow: '2px 18px 25px rgba(4, 2, 0.6, 0.3)'
      }}
    >
      <Box
        height={'100%'}
        display={'flex'}
        flexDirection={'column'}
        alignItems={'center'}
        justifyContent={'space-between'}
      >
        <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
        >
        </Box>
        <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          gap={'70px'}
        >
          {items.map((item, index) => {
            return <LeftBarItem
              key={index}
              item={item}
              router={routerList[index]}
              isSelect={location.pathname === routerList[index]} />
          })}
        </Box>
        <LogoutIcon sx={{ color: theme.palette.text.secondary, cursor: 'pointer', width: '50px', height: '50px' }}
          onClick={handleLogout} />
      </Box>
    </Box>
  )
}

export default LeftBar
