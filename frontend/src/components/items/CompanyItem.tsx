import React from 'react'
import { Box, Typography } from '@mui/material'

export const CompanyItem = ({ title }: { title: string }) => {
  return (
    <Box
      width={'300px'}
      height={'90px'}
      display={'flex'}
      justifyContent={'center'}
      alignItems={'center'}
      padding={'20px'}
      borderRadius={'10px'}
      border={'1px solid #000'}
      boxShadow={'0px 4px 4px rgba(0, 0, 0, 0.25)'}
      sx={{
        '&:hover': {
          backgroundColor: '#f5f5f5'
        },
        cursor: 'pointer',
        backgroundColor: 'rgba(243, 245, 249, .5)'
      }}
    >
      <Typography fontSize={20}>{title}</Typography>
    </Box>
  )
}
