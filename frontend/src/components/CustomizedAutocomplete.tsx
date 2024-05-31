import React from 'react'

import MuiAutocomplete from '@mui/material/Autocomplete'
import Popper from '@mui/material/Popper'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import type { InputProps } from '@mui/material/Input'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import type { AutocompleteProps as MuiAutocompleteProps } from '@mui/material/Autocomplete'
import { TextField, useTheme } from '@mui/material'

interface Option<T> {
  title: string
  value: T
}

type CustomAutocomplete<T> = Omit<MuiAutocompleteProps<
Option<T>,
undefined,
undefined,
undefined
>, 'renderInput' | 'onChange' | 'onInputChange'>

export type AutocompleteProps<T> = CustomAutocomplete<T> & {
  options: Array<Option<T>>
  onChange: (value: Option<T> | null) => void
  onInputChange?: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  textFieldProps?: InputProps
}

export default function CustomizedAutocomplete<T> ({
  options,
  textFieldProps,
  onChange,
  onInputChange,
  title,
  ...rest
}: AutocompleteProps<T>) {
  const ref = React.useRef(null)
  const theme = useTheme()
  return (
    <MuiAutocomplete
      options={options || []}
      getOptionLabel={(option) => option.title}
      onChange={(e, newValue) => {
        onChange(newValue)
      }}
      PopperComponent={(popperProps) => (
        <Popper
          ref={ref}
          sx={{
            offset: 0,
            paddingTop: '5px',
            '& .MuiPaper-root': {
              boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)',
              transition: 'none',
              border: '1px solid #E0E0E0',
              borderRadius: '1px',
              backgroundColor: theme.palette.primary.light
            }
          }}
          {...popperProps}
        >
          {popperProps.children}
        </Popper>
      )}
      sx={{
        '& .MuiAutocomplete-inputRoot': {
          backgroundColor: theme.palette.primary.light,
          borderRadius: '8px',
          height: '35px'
        },
        '& .MuiAutocomplete-input': {
          padding: '0 !important',
          fontSize: '14px',
          color: theme.palette.text.primary
        },
        ...rest.sx
      }}
      {...rest}
      renderInput={(params) => (
        <TextField
          {...params}
          onChange={onInputChange}
          title={title ?? ''}
          InputProps={{
            ...params.InputProps,
            ...textFieldProps
          }}
        />
      )}
    />
  )
}
