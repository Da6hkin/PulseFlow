import React from 'react'
import { ThemeProvider } from '@mui/material/styles'
import { CssBaseline } from '@mui/material'
import theme from './theme'
import Routes from './routes'
import { Provider } from 'react-redux'
import { store } from './store'
import ErrorBoundary from './pages/ErrorBoundary'

function App () {
  return (
    <>
      <CssBaseline />
      <ErrorBoundary name="App">
        <ThemeProvider theme={theme}>
          <Provider store={store}>
            <Routes />
          </Provider>
        </ThemeProvider>
      </ErrorBoundary>
    </>
  )
}

export default App
