import React from 'react'
import { Box, useTheme } from '@mui/material'
import { useNavigate } from 'react-router-dom'

const LeftBarItem = ({ item, isSelect, router }: { item: string, isSelect: boolean, router: string }) => {
  const theme = useTheme()
  const navigate = useNavigate()

  const handleNavigate = () => {
    navigate(router)
  }

  return (
    <Box
      sx={{
        color: theme.palette.text.primary,
        cursor: 'pointer',
        borderBottom: isSelect ? `4px solid ${theme.palette.text.secondary}` : 'none',
        fontSize: '18px',
        fontWeight: 700
      }}
      onClick={handleNavigate}
    >
      {item}
    </Box>
  )
}

export default LeftBarItem
