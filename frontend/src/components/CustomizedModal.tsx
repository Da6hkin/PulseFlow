import React from 'react'

import Dialog from '@mui/material/Dialog'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import HighlightOffIcon from '@mui/icons-material/HighlightOff'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { SxProps, Theme, useTheme } from '@mui/material'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import type { DialogProps } from '@mui/material/Dialog'
import { red } from '@mui/material/colors'

type PopupProps = Omit<DialogProps, 'maxWidth'> & {
  title: string | React.ReactNode
  titleSx?: SxProps<Theme>
  children: React.ReactNode
  maxWidth?: string
  handleClose?: () => void
  action: () => void
}

export default function CustomizedModal ({
  title,
  titleSx,
  children,
  handleClose,
  sx,
  maxWidth = '596px',
  action,
  ...rest
}: PopupProps) {
  const theme = useTheme()

  const handleOnClose = () => {
    handleClose?.()
  }

  return (
    <Dialog
      {...rest}
      sx={{
        '& .MuiDialog-container .MuiPaper-root': {
          width: '100%',
          maxWidth,
          borderRadius: '10px',
          overflow: 'hidden'
        },
        ...sx
      }}
    >
      <Box
        display="flex"
        flexDirection="column"
      >
        <Box
          display="flex"
          flexDirection="column"
          minHeight={'300px'}
          padding={'24px'}
          gap={'30px'}
          sx={{
            backgroundColor: theme.palette.primary.light
          }}
        >
          <HighlightOffIcon sx={{
            position: 'absolute',
            top: '7px',
            right: '9px',
            cursor: 'pointer',
            width: '30px',
            height: '30px',
            color: theme.palette.text.primary,
            backgroundColor: theme.palette.primary.light,
            borderRadius: '50%',
            zIndex: 1000
          }}
          onClick={handleClose} />
          <Box
            display="flex"
            flexDirection="row"
            justifyContent="space-between"
            alignItems="center"
            width='100%'
          >
            <Title title={title ?? ''} titleSx={titleSx} />
          </Box>
          {children}
        </Box>
        <Box
          display="flex"
          justifyContent="end"
          alignItems="center"
          padding={'35px'}
          sx={{
            backgroundColor: theme.palette.text.secondary
          }}
        >
          <Box
            sx={{
              cursor: 'pointer',
              color: red[500],
              fontSize: '14px',
              fontWeight: 600,
              padding: '10px 20px',
              borderRadius: '8px',
              backgroundColor: theme.palette.secondary.light
            }}
            onClick={handleOnClose}
          >
            Скасувати
          </Box>
          <Box
            sx={{
              cursor: 'pointer',
              color: theme.palette.text.primary,
              fontSize: '14px',
              fontWeight: 600,
              padding: '10px 20px',
              borderRadius: '8px',
              backgroundColor: theme.palette.primary.light,
              marginLeft: '20px'
            }}
            onClick={action}
          >
            Зробити
          </Box>
        </Box>
      </Box>
    </Dialog >
  )
}

interface TitleProps {
  title: string | React.ReactNode | undefined
  titleSx?: SxProps<Theme>
}

function Title ({ title, titleSx }: TitleProps) {
  const theme = useTheme()
  return (
    <Typography
      variant='h6'
      fontWeight={700}
      color={theme.palette.text.primary}
      sx={titleSx}
    >
      {title}
    </Typography>
  )
}
