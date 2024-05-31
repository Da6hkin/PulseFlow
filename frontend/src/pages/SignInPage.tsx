import React from 'react'
import authImage from 'src/assets/logo-pulse-flow.svg'
import {
  Box, styled, Modal as MuiModal, useTheme, Typography,
  Button,
  InputAdornment,
  IconButton
} from '@mui/material'
import { Visibility, VisibilityOff } from '@mui/icons-material'
import { serverURL } from 'src/config'
import axios from 'axios'
import { useDispatch } from 'react-redux'
import { setEmailState } from 'src/store/users'
import CustomizedInput from 'src/components/CustomizedInput'

const SignInPage: React.FC = () => {
  const theme = useTheme()
  const dispatch = useDispatch()
  const img = <img src={authImage} alt="img" />

  const [password, setPassword] = React.useState('')
  const [showPassword, setShowPassword] = React.useState(false)
  const [email, setEmail] = React.useState('')
  const [signUp, setSignUp] = React.useState(false)
  const [name, setName] = React.useState('')
  const [surname, setSurname] = React.useState('')
  const [error, setError] = React.useState('')

  const handleChangeEmail: (event: React.ChangeEvent<HTMLInputElement>) => void = (event) => {
    setEmail(event.target.value)
  }

  const handleChangePassword: (event: React.ChangeEvent<HTMLInputElement>) => void = (event) => {
    setPassword(event.target.value)
  }

  const handleClickShowPassword = () => setShowPassword((show) => !show)

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault()
  }

  const handleSetUp = () => setSignUp((sign) => !sign)

  const handleChangeName: (event: React.ChangeEvent<HTMLInputElement>) => void = (event) => {
    setName(event.target.value)
  }

  const handleChangeSurName: (event: React.ChangeEvent<HTMLInputElement>) => void = (event) => {
    setSurname(event.target.value)
  }

  const handleAuthLogin = async () => {
    // await localStorage.setItem('token', 'token')
    // window.location.reload()
    // setError('')

    if (!email || !password || (signUp && (!name || !surname))) {
      setError('Email, password, name, surname are required')
    } else if (signUp && name && password && surname) {
      const authObject = {
        name,
        surname,
        password,
        email,
        disabled: false
      }
      await axios.post(`${serverURL}/api/user`, authObject)
        .then((res) => {
          if (res?.data) {
            setSignUp(false)
            setName('')
            setSurname('')
            setError('')
          }
        })
        .catch((err) => {
          setError(err?.response?.data?.message || 'Something went wrong')
        })
    } else if (!signUp && email && password) {
      const authObject = {
        email,
        password
      }
      await axios.post(`${serverURL}/api/auth/login`, authObject)
        .then((res) => {
          if (res?.data?.token) {
            dispatch(setEmailState(email))
            localStorage.setItem('token', res?.data?.token)
            window.location.reload()
            setError('')
            setEmail('')
            setPassword('')
          }
        })
        .catch((err) => {
          setError(err?.response?.data?.message || 'Something went wrong')
        })
    }
  }

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
          width: '100vw',
          overflow: 'hidden'
        }}
      >
        {img}
      </Box>
      <CustomizedModal open>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            alignItems: 'center',
            height: '546px'
          }}
        >
          <Box
            sx={{
              fontSize: '32px',
              fontStyle: 'normal',
              fontWeight: 'bold',
              lineHeight: '40px',
              marginBottom: '24px',
              marginTop: '8px',
              color: theme.palette.text.primary
            }}
          >{!signUp ? 'Sign In' : 'Sign Up'}</Box>

          <Box sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flexStart',
            gap: '24px'
          }}>

            {signUp && <Box sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'flexStart'
            }}>
              <Typography variant='body1' sx={{
                color: theme.palette.text.primary,
                marginBottom: '4.5px'
              }}>Name</Typography>
              <CustomizedInput
                value={name}
                type='text'
                placeholder='Enter Name'
                onChange={handleChangeName}
              />
            </Box>}

            {signUp && <Box sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'flexStart'
            }}>
              <Typography variant='body1' sx={{
                color: theme.palette.text.primary,
                marginBottom: '4.5px'
              }}>SurName</Typography>
              <CustomizedInput
                value={surname}
                type='text'
                placeholder='Enter SurName'
                onChange={handleChangeSurName}
              />
            </Box>}

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
                value={email}
                type='email'
                placeholder='Enter Email'
                onChange={handleChangeEmail}
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
              }}>Password</Typography>
              <CustomizedInput
                placeholder='Enter Password'
                value={password}
                onChange={handleChangePassword}
                id="filled-adornment-password"
                type={showPassword ? 'text' : 'password'}
                InputProps={{
                  endAdornment:
                    < InputAdornment position="end" >
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                }}
              />
            </Box>
          </Box>

          <Typography variant='body1' sx={{
            color: theme.palette.text.primary,
            marginBottom: '4.5px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center'
          }}>{signUp ? 'You have account' : 'You not have account?'}
            <Button onClick={handleSetUp}>{signUp ? 'Sign In' : 'Sign Up'}</Button>
          </Typography>

          {error && <Typography variant='body1' sx={{
            color: theme.palette.error.main,
            marginBottom: '4.5px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center'
          }}>{error}</Typography>}

          <Button
            onClick={handleAuthLogin}
            sx={{
              width: '381px',
              height: '43px',
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
            >{!signUp ? 'Sign In' : 'Sign Up'}</Typography>
          </Button>
        </Box>
      </CustomizedModal >
    </>
  )
}

export default SignInPage

const CustomizedModal = styled(MuiModal)(`
display: flex;
flex-direction: column;
justify-content: space-between;
align-items: center;
.MuiBackdrop-root {
  position: absolute;
  top: 50%;
  left: 50%;
  padding: 24px;
  transform: translate(-50%, -50%);
  width: 429px;
  min-height: 600px;
  border-radius: 24px;
  border: 3px solid rgba(65, 65, 213, 0.30);
  background: rgba(255, 255, 255, 0.60);
  box-shadow: 0px 4px 15px 0px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(25px);
}
`)
