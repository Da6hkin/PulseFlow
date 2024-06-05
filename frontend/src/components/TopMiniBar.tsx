import React from 'react'
import { Box, Button, Typography, useTheme } from '@mui/material'
import { ReactComponent as Logo } from '../assets/logo-pulse-flow.svg'
import { useLocation, useNavigate } from 'react-router-dom'
import Time from './Time'
import LeftBarItem from './items/LeftBarItem'
import { useSelector, useDispatch } from 'react-redux'
import { selectCurrentCompany } from 'src/store/company'
import { useProjectIsPmQuery } from 'src/store/project'
import { setOpenModal } from 'src/store/task'

const items = ['ЗАВДАННЯ', 'МОЯ КОМАНДА']

const TopMiniBar = () => {
  const theme = useTheme()
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const location = useLocation()
  const projectId = location.pathname.split('/')[2]
  const isTaskLocation = location.pathname.includes('task')
  const currentCompany = useSelector(selectCurrentCompany)
  const { data: isProjectManager } = useProjectIsPmQuery(projectId)

  const routerList = [
    `/task/${projectId}`,
    `/team/${projectId}`
  ]

  const handleNavigate = () => {
    navigate('/')
  }

  const handleOpenModal = () => {
    dispatch(setOpenModal(true))
  }

  return (
    <Box
      sx={{
        width: '100vw',
        height: '100px',
        backgroundColor: theme.palette.primary.light,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '24px 80px',
        boxShadow: '2px 18px 25px rgba(4, 2, 0.6, 0.1)'
      }}
    >
      <Box
        display={'flex'}
        alignItems={'center'}
        gap={'65px'}
      >
        <Box
          display={'flex'}
          alignItems={'center'}
          onClick={handleNavigate}
          sx={{
            cursor: 'pointer'
          }}
        >
          <Logo width={'70px'} height={'70px'} />
        </Box>
        <Box
          sx={{
            fontSize: '24px',
            fontStyle: 'normal',
            fontWeight: 'bold',
            lineHeight: '30px',
            color: theme.palette.primary.dark
          }}
        >{currentCompany?.name}</Box>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            gap: '65px',
            marginTop: '7px'
          }}
        >
          {items.map((item, index) => {
            return <LeftBarItem
              key={index}
              item={item}
              router={routerList[index]}
              isSelect={location.pathname.includes(routerList[index])} />
          })}
        </Box>
      </Box>
      <Box
        display={'flex'}
        alignItems={'center'}
      >
        {isTaskLocation && isProjectManager && <Button
          onClick={handleOpenModal}
          sx={{
            width: '100px',
            height: '40px',
            marginRight: '40px',
            borderRadius: '12px',
            backgroundColor: theme.palette.primary.main,
            '&:hover': {
              backgroundColor: theme.palette.primary.dark
            }
          }}>
          <Typography variant='button'
            sx={{
              textTransform: 'capitalize',
              color: theme.palette.text.primary
            }}
          >+ Додати</Typography>
        </Button>}
        <Time />
      </Box>
    </Box>
  )
}

export default TopMiniBar
