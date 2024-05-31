import React, { useEffect, useState } from 'react'

import AccessTimeIcon from '@mui/icons-material/AccessTime'
import { Box, useTheme } from '@mui/material'
import Typography from '@mui/material/Typography'
import { format } from 'date-fns'

export default function Time () {
  const [currentTime, setCurrentTime] = useState(() => new Date())
  const theme = useTheme()

  const currentDate = format(new Date(), 'dd MMM, yyyy')
  const cuurrentTimeFormated = format(currentTime, 'HH:mm')
  const dayOfWeek = format(currentTime, 'EEEE')

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => {
      clearInterval(interval)
    }
  }, [])

  return (
    <Box
      display="flex"
      flexDirection="column"
      gap={'5px'}
    >
      <Typography variant='body2'>
        {dayOfWeek}
      </Typography>
      <Box display={'flex'} alignItems={'center'} gap={'14px'}>
        <Typography variant='body2'>
          {currentDate}
        </Typography>
        <Box display="flex" gap={'4px'}>
          <AccessTimeIcon sx={{ color: theme.palette.text.secondary, width: '20px', height: '20px' }} />
          <Typography variant='body2'>
            {cuurrentTimeFormated}
          </Typography>
        </Box>
      </Box>
    </Box>
  )
}
