import React, { useEffect, useState } from 'react'
import { Box, Typography } from '@mui/material'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import { format } from 'date-fns'
import { uk } from 'date-fns/locale'
import { useTheme } from '@mui/material/styles'

export default function Time () {
  const [currentTime, setCurrentTime] = useState(() => new Date())
  const theme = useTheme()

  const currentDate = format(new Date(), 'dd MMMM, yyyy', { locale: uk })
  const currentTimeFormatted = format(currentTime, 'HH:mm', { locale: uk })
  const dayOfWeek = format(currentTime, 'EEEE', { locale: uk })

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
            {currentTimeFormatted}
          </Typography>
        </Box>
      </Box>
    </Box>
  )
}
