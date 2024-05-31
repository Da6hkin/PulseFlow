import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

interface RequestUser {
  name: string
  surname: string
  password: string
  email: string
  disabled: boolean
}

export interface IUser {
  id?: string
  name: string
  surname: string
  email: string
  disabled: boolean
  password?: string
}

interface SearchUserRequest {
  email: string
  disabled?: boolean
  id?: string
  order_by?: '-id' | 'id'
}

interface PutUser {
  password?: string
  disabled?: boolean
}

export const UserApi = createApi({
  reducerPath: 'UserApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${serverURL}/api/user`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token')
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['User'],
  endpoints: (builder) => ({
    createUser: builder.mutation<RequestUser, IUser>({
      query: (user) => ({
        url: '',
        method: 'POST',
        body: user
      }),
      invalidatesTags: [{ type: 'User', id: 'LIST' }]
    }),
    searchUser: builder.query<IUser[], SearchUserRequest>({
      query: (params) => ({
        url: '/search',
        method: 'POST',
        body: params
      }),
      providesTags: [{ type: 'User', id: 'LIST' }]
    }),
    getUser: builder.query<IUser, string>({
      query: (userId) => ({
        url: `/${userId}`,
        method: 'GET'
      })
    }),
    updateUser: builder.mutation<IUser, { user: PutUser, userId: string }>({
      query: ({ user, userId }) => ({
        url: `/${userId}`,
        method: 'PUT',
        body: user
      }),
      invalidatesTags: [{ type: 'User', id: 'LIST' }]
    }),
    // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
    deleteUser: builder.mutation<void, string>({
      query: (userId: string) => ({
        url: `/${userId}`,
        method: 'DELETE'
      }),
      invalidatesTags: [{ type: 'User', id: 'LIST' }]
    }),
    getMe: builder.query<IUser, void>({
      query: () => '/me'
    })
  })
})

export const {
  useCreateUserMutation,
  useSearchUserQuery,
  useGetUserQuery,
  useUpdateUserMutation,
  useDeleteUserMutation,
  useGetMeQuery
} = UserApi

interface UserState {
  users: IUser[]
  email: string
  currentUser: IUser
}

const initialState: UserState = {
  users: [],
  email: '',
  currentUser: {
    id: '',
    name: '',
    surname: '',
    email: '',
    disabled: false
  }
}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserState: (state, action: PayloadAction<IUser[]>) => {
      state.users = action.payload
    },
    setEmailState: (state, action: PayloadAction<string>) => {
      state.email = action.payload
    },
    setCurrentUserState: (state, action: PayloadAction<IUser>) => {
      state.currentUser = action.payload
    }
  }
})

export const { setUserState, setEmailState, setCurrentUserState } = userSlice.actions

export const selectUserState = (state: RootState) => state?.users.users
export const selectEmailState = (state: RootState) => state?.users.email
export const selectCurrentUserState = (state: RootState) => state?.users.currentUser

export default userSlice.reducer
