import React from 'react'
import { Box, IconButton, InputAdornment, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import KanbanBoard from 'src/components/kanban/KanbanBoard'
import CustomizedInput from 'src/components/CustomizedInput'
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline'

const ChatTextMessage = ({ message }: { message: string }) => {
  return (
    <Box
      sx={{
        backgroundColor: 'white',
        borderRadius: '10px',
        border: '0.5px solid #e0e0e0',
        padding: '10px',
        gap: '10px',
        width: '100%',
        whiteSpace: 'pre-wrap',
        wordWrap: 'break-word'
      }}
    >
      <Typography>
        {message}
      </Typography>
    </Box>
  )
}

const TaskPage: React.FC = () => {
  const [chatMessages, setChatMessages] = React.useState<string[]>([])
  const [message, setMessage] = React.useState('')

  const handleSetMessage = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(e.target.value)
  }

  const handlePushMessage = () => {
    setChatMessages([...chatMessages, message])
    setMessage('')
  }

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
          Task Page
        </Typography>
        <Box
          width={'100%'}
          display={'flex'}
          justifyContent={'space-between'}
          alignItems={'start'}>

          <KanbanBoard />
          <Box
            display={'flex'}
            flexDirection={'column'}
            justifyContent={'space-between'}
            maxWidth={'500px'}
            height={'750px'}
            sx={{
              backgroundColor: 'aliceblue',
              borderRadius: '10px',
              border: '3px solid #e0e0e0',
              padding: '15px',
              marginTop: '16px'
            }}
          >
            <Box
              display={'flex'}
              flexDirection={'column'}
              width={'100%'}
              height={'100%'}
              sx={{
                backgroundColor: 'aliceblue',
                overflowY: 'auto',
                gap: '8px'
              }}
            >
              {chatMessages?.map((message, index) => (
                <ChatTextMessage key={index} message={message} />
              ))}
            </Box>
            <CustomizedInput
              value={message}
              type='text'
              onChange={handleSetMessage}
              placeholder='Enter Message'
              sx={{
                position: 'relative',
                bottom: '0',
                marginTop: '20px',
                '& .MuiOutlinedInput-root': {
                  width: '100%'
                }
              }}
              InputProps={{
                endAdornment:
                  < InputAdornment position="end" >
                    <IconButton
                      onClick={handlePushMessage}
                      edge="end"
                    >
                      <AddCircleOutlineIcon />
                    </IconButton>
                  </InputAdornment>
              }}
            />
          </Box>
        </Box>
      </Box>
    </WrapperPage>
  )
}

export default TaskPage
