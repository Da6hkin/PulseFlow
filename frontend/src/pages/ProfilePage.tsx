import React, { useEffect } from 'react'
import { Box, Typography, useTheme } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import { selectCurrentUserState, setCurrentUserState, useGetMeQuery } from 'src/store/users'
import CustomizedInput from 'src/components/CustomizedInput'
import { useSelector, useDispatch } from 'react-redux'
import { setCompanyState, useGetMeCompanyQuery } from 'src/store/company'

const ProfilePage: React.FC = () => {
  const theme = useTheme()
  const dispatch = useDispatch()
  const currentUser = useSelector(selectCurrentUserState)
  const { data: user } = useGetMeQuery()
  const { data: companyData } = useGetMeCompanyQuery()

  useEffect(() => {
    companyData && dispatch(setCompanyState(companyData))
  }, [companyData])

  useEffect(() => {
    user && dispatch(setCurrentUserState(user))
  }, [user])

  return (
    <WrapperPage>
      <Box
        display={'flex'}
        flexDirection={'column'}
        justifyContent={'start'}
        alignItems={'start'}
        gap={'30px'}
      >
        <Typography fontSize={30} >
          Мій профіль
        </Typography>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flexStart'
        }}>
          <Typography variant='body1' sx={{
            color: theme.palette.text.primary,
            marginBottom: '4.5px'
          }}>Ім’я</Typography>
          <CustomizedInput
            value={currentUser?.name}
            type='text'
          />
        </Box>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flexStart'
        }}>
          <Typography variant='body1' sx={{
            color: theme.palette.text.primary,
            marginBottom: '4.5px'
          }}>Прізвище</Typography>
          <CustomizedInput
            value={currentUser?.surname}
            type='text'
          />
        </Box>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flexStart'
        }}>
          <Typography variant='body1' sx={{
            color: theme.palette.text.primary,
            marginBottom: '4.5px'
          }}>Імейл</Typography>
          <CustomizedInput
            value={currentUser?.email}
            type='text'
          />
        </Box>
      </Box>
    </WrapperPage>
  )
}

export default ProfilePage
