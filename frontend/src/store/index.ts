// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { configureStore, combineReducers, type Middleware, isRejectedWithValue } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import usersReduser, { UserApi } from './users'
import companyReduser, { CompanyApi } from './company'
import projectReduser, { ProjectApi } from './project'
import employeeReduser, { EmployeeApi } from './employee'
import taskReduser, { TaskApi } from './task'
import chatReduser, { ChatApi } from './chat'

const unauthenticatedMiddleware: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action) &&
    (action.payload?.status === 401 || action.payload?.status === 403)) {
    localStorage.removeItem('token')
    window.location.reload()
  }
  return next(action)
}

const reducers = {
  users: usersReduser,
  company: companyReduser,
  project: projectReduser,
  employee: employeeReduser,
  task: taskReduser,
  chat: chatReduser,
  [UserApi.reducerPath]: UserApi.reducer,
  [CompanyApi.reducerPath]: CompanyApi.reducer,
  [ProjectApi.reducerPath]: ProjectApi.reducer,
  [EmployeeApi.reducerPath]: EmployeeApi.reducer,
  [TaskApi.reducerPath]: TaskApi.reducer,
  [ChatApi.reducerPath]: ChatApi.reducer
}

const rootReducer = combineReducers<typeof reducers>(reducers)

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false
    })
      .concat(UserApi.middleware)
      .concat(unauthenticatedMiddleware)
      .concat(CompanyApi.middleware)
      .concat(ProjectApi.middleware)
      .concat(EmployeeApi.middleware)
      .concat(TaskApi.middleware)
      .concat(ChatApi.middleware),
  devTools: process.env.NODE_ENV !== 'production'
})

export type RootState = ReturnType<typeof store.getState>

setupListeners(store.dispatch)
