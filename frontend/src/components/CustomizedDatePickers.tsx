import React from 'react'
import {
  DateTimePicker as MuiDateTimePicker,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  type DateTimePickerProps
} from '@mui/x-date-pickers/DateTimePicker'
import { styled } from '@mui/material'

function DateTimePicker ({ ...rest }) {
  return (
    <MuiDateTimePicker
      format='dd/MM/yyyy HH:mm:ss'
      sx={{
        width: '100%',
        borderRadius: '16px',
        height: '38px',
        '& .MuiInputBase-root': {
          '& fieldset': {
            border: '1px solid #e0e0e0',
            borderRadius: '16px'
          },
          '&:hover fieldset': {
            borderColor: '#e0e0e0'
          },
          '&.Mui-focused fieldset': {
            borderColor: '#e0e0e0'
          }
        }
      }}
      {...rest}
    />
  )
}

const CustomizedDatePickers = styled(DateTimePicker)(`  
.MuiInputBase-root{
  background: #FFFFFF;
  border-radius: 16px;
  padding: 10px 16px;
}
.MuiPaper-root{
  background: #FFFFFF;
}
input{
  padding: 0;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  color: #393E51;
}
label{
  color: #6B6B6B;
  font-size: 18px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  margin-top: -9px;
  &.Mui-focused{
    margin-top: -4px;
  }
}
`)

export default CustomizedDatePickers
