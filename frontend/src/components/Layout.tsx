import React from 'react'

import { Outlet } from 'react-router-dom'
import Box from '@mui/material/Box'
import TopBar from './TopBar'
import LeftBar from './LeftBar'
import { useTheme } from '@mui/material'

const zoom = 1

export default function Layout () {
  const theme = useTheme()
  return (
    <Box
      height={'100%'}
      width={'100%'}
      display="flex"
      flexDirection="column"
      justifyContent={'flex-start'}
      sx={{
        transform: `scale(${zoom})`,
        transformOrigin: 'left top',
        width: `calc(100% / ${zoom})`,
        height: `calc(100% / ${zoom})`,
        backgroundColor: theme.palette.background.default,
        overflowX: 'hidden'
      }}
    >
      <TopBar />
      <Box
        display="flex"
        justifyContent="flex-start"
        sx={{
          width: '100%',
          height: '100%'
        }}
      >
        <LeftBar />
        <Box
          display="flex"
          justifyContent="flex-start"
          alignItems="center"
          sx={{
            width: '100%',
            height: '100%',
            overflow: 'auto'
          }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}
