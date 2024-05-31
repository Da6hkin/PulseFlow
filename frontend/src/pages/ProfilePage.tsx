import React, { useEffect } from 'react'
import { Box, Typography, useTheme } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { useGetMeQuery, IUser, setCurrentUserState } from 'src/store/users'
import { useDispatch } from 'react-redux'
import CustomizedInput from 'src/components/CustomizedInput'

const ProfilePage: React.FC = () => {
  const dispatch = useDispatch()
  const theme = useTheme()
  const { data } = useGetMeQuery()

  useEffect(() => {
    data && dispatch(setCurrentUserState(data))
  }, [data])

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
          }}>Name</Typography>
          <CustomizedInput
            value={data?.name}
            type='text'
            placeholder='Enter Name'
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
          }}>SurName</Typography>
          <CustomizedInput
            value={data?.surname}
            type='text'
            placeholder='Enter SurName'
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
          }}>Email</Typography>
          <CustomizedInput
            value={data?.email}
            type='text'
            placeholder='Enter Email'
          />
        </Box>
      </Box>
    </WrapperPage>
  )
}

export default ProfilePage
