import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

export interface RequestEmployee {
  user?: number
  company?: number
  is_admin: boolean
  disabled: boolean
}

export interface IEmployee {
  id?: number
  user: {
    id: number
    name: string
    surname: string
    email: string
    disabled: boolean
  }
  company: {
    id: number
    name: string
    unique_identifier: string
    website: string
    logo: string
  }
  is_admin: boolean
  disabled: boolean
  project_manager?: boolean
}

interface UpdateEmployee {
  is_admin: boolean
}

interface SearchEmployeeRequest {
  id?: number
  is_admin?: boolean
  disabled?: boolean
  company?: number
  order_by?: '-id' | 'id' | 'user' | '-user' | 'company' | '-company'
}

export const EmployeeApi = createApi({
  reducerPath: 'EmployeeApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${serverURL}/api/employee`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token')
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['Employee'],
  endpoints: (builder) => ({
    createEmployee: builder.mutation<IEmployee, RequestEmployee>({
      query: (employee) => ({
        url: '',
        method: 'POST',
        body: employee
      }),
      invalidatesTags: [{ type: 'Employee', id: 'LIST' }]
    }),
    searchEmployee: builder.query<IEmployee[], SearchEmployeeRequest>({
      query: (arg: SearchEmployeeRequest) => ({
        url: `/search${arg.company ? `?company=${arg.company}` : ''}`,
        method: 'GET'
      }),
      providesTags: [{ type: 'Employee', id: 'LIST' }]
    }),
    getEmployee: builder.query<IEmployee, string>({
      query: (employeeId) => ({
        url: `/${employeeId}`,
        method: 'GET'
      })
    }),
    updateEmployee: builder.mutation<IEmployee, { employee: UpdateEmployee, employeeId: string }>({
      query: ({ employee, employeeId }) => ({
        url: `/${employeeId}`,
        method: 'PUT',
        body: employee
      }),
      invalidatesTags: [{ type: 'Employee', id: 'LIST' }]
    }),
    employeeInvate: builder.mutation<IEmployee, { email: string, company_id: number }>({
      query: ({ email, company_id }) => ({
        url: '/invite',
        method: 'POST',
        body: { email, company_id }
      }),
      invalidatesTags: [{ type: 'Employee', id: 'LIST' }]
    }),
    getEmployeeByCompany: builder.query<IEmployee[], number>({
      query: (companyId) => ({
        url: `/byCompany/${companyId}`,
        method: 'GET'
      })
    })
  })
})

export const {
  useCreateEmployeeMutation,
  useSearchEmployeeQuery,
  useGetEmployeeQuery,
  useUpdateEmployeeMutation,
  useEmployeeInvateMutation,
  useGetEmployeeByCompanyQuery
} = EmployeeApi

interface EmployeeState {
  employee: IEmployee[]
}

const initialState: EmployeeState = {
  employee: []
}

const employeeSlice = createSlice({
  name: 'employee',
  initialState,
  reducers: {
    setEmployeeState: (state, action: PayloadAction<IEmployee[]>) => {
      state.employee = action.payload
    }
  }
})

export const { setEmployeeState } = employeeSlice.actions

export const selectEmployeeState = (state: RootState) => state?.employee.employee

export default employeeSlice.reducer
