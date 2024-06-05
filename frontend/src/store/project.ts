import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

interface RequestProject {
  company: number
  name: string
  description: string
  start_date?: Date
  end_date?: Date
  income?: number
}

export interface IProject {
  id: number
  company: {
    id: number
    name: string
    unique_identifier: string
    website: string
    logo: string
  }
  name: string
  description: string
  start_date: string
  end_date: string
  income: number
}

interface UpdateProject {
  description?: string
  start_date?: string
  end_date?: string
  income?: number
}

interface SearchProjectRequest {
  company?: number
  end_date?: string
  id?: number
  income?: number
  name?: string
  order_by?: '-id' | 'id' | '-name' | 'name' | '-start_date' | 'start_date' | '-end_date' | 'end_date' | '-income' | 'income'
}

export const ProjectApi = createApi({
  reducerPath: 'ProjectApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${serverURL}/api/project`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token')
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['Project'],
  endpoints: (builder) => ({
    createProject: builder.mutation<IProject, RequestProject>({
      query: (project) => ({
        url: '',
        method: 'POST',
        body: project
      }),
      invalidatesTags: [{ type: 'Project', id: 'LIST' }]
    }),
    searchProject: builder.query<IProject[], SearchProjectRequest>({
      query: ({ company }) => ({
        url: `/search${company ? `?company=${company}` : ''}`,
        method: 'GET'
      }),
      providesTags: [{ type: 'Project', id: 'LIST' }]
    }),
    getProject: builder.query<IProject, string>({
      query: (projectId) => ({
        url: `/${projectId}`,
        method: 'GET'
      })
    }),
    updateProject: builder.mutation<IProject, { project: UpdateProject, projectId: string }>({
      query: ({ project, projectId }) => ({
        url: `/${projectId}`,
        method: 'PUT',
        body: project
      }),
      invalidatesTags: [{ type: 'Project', id: 'LIST' }]
    }),
    projectIsPm: builder.query<IProject, string>({
      query: (projectId) => ({
        url: `/is_pm/${projectId}`,
        method: 'GET'
      })
    }),
    getProjectFinance: builder.query({
      query: (projectId: string) => ({
        url: `/finance/${projectId}`,
        method: 'GET'
      })
    })
  })
})

export const {
  useCreateProjectMutation,
  useSearchProjectQuery,
  useGetProjectQuery,
  useUpdateProjectMutation,
  useProjectIsPmQuery,
  useGetProjectFinanceQuery
} = ProjectApi

interface ProjectState {
  project: IProject[]
}

const initialState: ProjectState = {
  project: []
}

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    setProjectState: (state, action: PayloadAction<IProject[]>) => {
      state.project = action.payload
    }
  }
})

export const { setProjectState } = projectSlice.actions

export const selectProjectState = (state: RootState) => state?.project.project

export default projectSlice.reducer
