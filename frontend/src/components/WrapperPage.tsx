import React from 'react'
import { Box } from '@mui/material'

const WrapperPage = ({ children }: { children: React.ReactNode }) => {
  const isMobile = window.innerWidth < 600

  return (
    <Box
      display={'flex'}
      justifyContent={'start'}
      alignItems={'start'}
      width={'100vw'}
      minWidth={'max-content'}
      height={'100vh'}
      padding={isMobile ? '10px 15px' : '50px 100px'}
    >
      {children}
    </Box>

  )
}

export default WrapperPage
