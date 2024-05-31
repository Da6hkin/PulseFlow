import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

interface RequestCompany {
  id: number
  name: string
  unique_identifier: string
  website: string
  logo?: string
}

export interface ICompany {
  id?: number
  name: string
  unique_identifier: string
  website?: string
  logo?: string
}

interface UpdateCompany {
  name?: string
  website?: string
  logo?: string
}

interface SearchCompanyRequest {
  id?: string
  name?: string
  order_by?: '-id' | 'id' | '-name' | 'name' |'-unique_identifier' | 'unique_identifier'
}

export const CompanyApi = createApi({
  reducerPath: 'CompanyApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${serverURL}/api/company`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token')
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['Company'],
  endpoints: (builder) => ({
    createCompany: builder.mutation<RequestCompany, FormData>({
      query: (company) => ({
        url: '',
        method: 'POST',
        body: company
      }),
      invalidatesTags: [{ type: 'Company', id: 'LIST' }]
    }),
    searchCompany: builder.query<ICompany[], SearchCompanyRequest>({
      query: (params) => ({
        url: '/search',
        method: 'GET',
        body: params
      }),
      providesTags: [{ type: 'Company', id: 'LIST' }]
    }),
    getCompany: builder.query<ICompany, string>({
      query: (companyId) => ({
        url: `/${companyId}`,
        method: 'GET'
      })
    }),
    updateCompany: builder.mutation<ICompany, { company: UpdateCompany, companyId: string }>({
      query: ({ company, companyId }) => ({
        url: `/${companyId}`,
        method: 'PUT',
        body: company
      }),
      invalidatesTags: [{ type: 'Company', id: 'LIST' }]
    }),
    getMe: builder.query<ICompany, void>({
      query: () => ({
        url: '/me',
        method: 'GET'
      })
    })
  })
})

export const {
  useCreateCompanyMutation,
  useSearchCompanyQuery,
  useGetCompanyQuery,
  useUpdateCompanyMutation,
  useGetMeQuery
} = CompanyApi

interface CompanyState {
  company: ICompany[]
  currentCompany?: ICompany
}

const initialState: CompanyState = {
  company: [],
  currentCompany: undefined
}

const companySlice = createSlice({
  name: 'company',
  initialState,
  reducers: {
    setCompanyState: (state, action: PayloadAction<ICompany[]>) => {
      state.company = action.payload
    },
    setCurrentCompany: (state, action: PayloadAction<ICompany>) => {
      state.currentCompany = action.payload
    }
  }
})

export const { setCompanyState, setCurrentCompany } = companySlice.actions

export const selectCompanyState = (state: RootState) => state?.company.company
export const selectCurrentCompany = (state: RootState) => state?.company.currentCompany

export default companySlice.reducer
