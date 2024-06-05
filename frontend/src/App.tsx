import React from 'react'
import { ThemeProvider } from '@mui/material/styles'
import { CssBaseline } from '@mui/material'
import theme from './theme'
import Routes from './routes'
import { Provider } from 'react-redux'
import { store } from './store'
import ErrorBoundary from './pages/ErrorBoundary'
import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'

function App () {
  return (
    <>
      <CssBaseline />
      <ErrorBoundary name="App">
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Provider store={store}>
              <Routes />
            </Provider>
          </LocalizationProvider>
        </ThemeProvider>
      </ErrorBoundary>
    </>
  )
}

export default App
