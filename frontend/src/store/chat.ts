import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

interface RequestChat {
  created_at?: string
  text: string
  project: number
  user: number
}

export interface IChat {
  id: number
  project: {
    id: number
    company: {
      id: number
      name: string
      unique_identifier: string
      website: string
    }
    name: string
    description: string
    start_date: string
    end_date: string
    income: number
  }
  user: {
    id: number
    name: string
    surname: string
    email: string
    disabled: boolean
  }
  text: string
  created_at: string
}

interface PutChat {
  text?: string
}

interface SearchChatRequest {
  created_at?: string
  id?: number
  order_by: '-id' | 'id' | '-created_at' | 'created_at' | '-project' | 'project' | '-user' | 'user' | '-text' | 'text'
}

export const ChatApi = createApi({
  reducerPath: 'ChatApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${serverURL}/api`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token')
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['Chat'],
  endpoints: (builder) => ({
    createChat: builder.mutation({
      query: (chat: RequestChat) => ({
        url: '/chat',
        method: 'POST',
        body: {
          text: chat.text,
          project: chat.project,
          user: chat.user
        }
      }),
      invalidatesTags: [{ type: 'Chat', id: 'LIST' }]
    }),
    searchChat: builder.query({
      query: (project: string) => ({
        url: `/chat/search${project ? `?project=${project}` : ''}`,
        method: 'GET'
      }),
      providesTags: [{ type: 'Chat', id: 'LIST' }]
    }),
    getChat: builder.query<IChat, string>({
      query: (chatId) => ({
        url: `/chat/${chatId}`,
        method: 'GET'
      })
    }),
    updateChat: builder.mutation<IChat, { chatId: string, text: string }>({
      query: ({ chatId, text }) => ({
        url: `/chat/${chatId}`,
        method: 'PUT',
        body: { text }
      }),
      invalidatesTags: [{ type: 'Chat', id: 'LIST' }]
    }),
    // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
    deleteChat: builder.mutation<void, string>({
      query: (chatId: string) => ({
        url: `/chat/${chatId}`,
        method: 'DELETE'
      }),
      invalidatesTags: [{ type: 'Chat', id: 'LIST' }]
    })
  })
})

export const {
  useCreateChatMutation,
  useSearchChatQuery,
  useGetChatQuery,
  useUpdateChatMutation,
  useDeleteChatMutation
} = ChatApi

interface ChatState {
  chats: IChat[]
}

const initialState: ChatState = {
  chats: []
}

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    setChatState: (state, action: PayloadAction<IChat[]>) => {
      state.chats = action.payload
    }
  }
})

export const { setChatState } = chatSlice.actions

export const selectChatState = (state: RootState) => state?.chat.chats

export default chatSlice.reducer
