import React from 'react'
import { Outlet } from 'react-router-dom'
import Box from '@mui/material/Box'
import { useTheme } from '@mui/material'
import TopMiniBar from './TopMiniBar'

const zoom = 1

export default function MiniLayout () {
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
      <TopMiniBar />
      <Outlet />
    </Box>
  )
}
