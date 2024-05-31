import { useEffect } from 'react'

export function useAuthWatchDog (afterLogin: () => void, afterLogout: () => void) {
  const isAuthenticated = localStorage.getItem('token') !== null

  useEffect(() => {
    if (isAuthenticated) {
      afterLogin?.()
    } else {
      afterLogout?.()
    }
  }, [isAuthenticated, afterLogin, afterLogout])
}
