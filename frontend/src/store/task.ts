import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { serverURL } from 'src/config'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { RootState } from '.'

export type IState = 'todo' | 'research' | 'in_progress' | 'testing' | 'done'
export type IRateType = 'fixed' | 'hour'

export enum EState {
  TODO = 'todo',
  RESEARCH = 'research',
  IN_PROGRESS = 'in_progress',
  TESTING = 'testing',
  DONE = 'done'
}

export enum ERateType {
  FIXED = 'fixed',
  HOUR = 'hour'
}

export const RateOptions = [
  { value: ERateType.FIXED, title: 'Фіксована' },
  { value: ERateType.HOUR, title: 'Погодинна' }
]

interface RequestTask {
  state: string
  priority: number
  actual_start_date: string
  actual_end_date: string
  name: string
  description: string
  planned_start_date: string
  planned_end_date: string
  project: number
}

export interface ITask {
  id: number
  project: {
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
  name: string
  state: string
  priority: number
  description: string
  planned_start_date: string
  planned_end_date: string
  actual_start_date: string
  actual_end_date: string
  hours_spent?: number
  assigned?: any
}

interface PutTask {
  state?: string
  priority?: number
  actual_start_date?: string
  actual_end_date?: string
  name?: string
  description?: string
  planned_start_date?: string
  planned_end_date?: string
  hours_spent?: number
}

interface SearchTaskRequest {
  actual_end_date?: string
  actual_start_date?: string
  name?: string
  id?: number
  project?: number
  order_by?: '-id' | 'id' | '-name' | 'name' | '-state' | 'state' | '-priority' |
  'priority' | '-actual_start_date' | 'actual_start_date' | '-actual_end_date' |
  'actual_end_date' | '-planned_start_date' | 'planned_start_date' | '-planned_end_date' | 'planned_end_date'
}

export const TaskApi = createApi({
  reducerPath: 'TaskApi',
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
  tagTypes: ['Task'],
  endpoints: (builder) => ({
    createTask: builder.mutation<RequestTask, ITask>({
      query: (task) => ({
        url: '/task',
        method: 'POST',
        body: task
      }),
      invalidatesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    searchTask: builder.query<ITask[], SearchTaskRequest>({
      query: ({ project }) => ({
        url: `/task/search${project ? `?project=${project}` : ''}`,
        method: 'GET'
      }),
      providesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    getTask: builder.query<ITask, string>({
      query: (taskId) => ({
        url: `/task/${taskId}`,
        method: 'GET'
      })
    }),
    updateTask: builder.mutation<ITask, { task: PutTask, taskId: number }>({
      query: ({ task, taskId }) => ({
        url: `/task/${taskId}`,
        method: 'PUT',
        body: task
      }),
      invalidatesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
    deleteTask: builder.mutation<void, string>({
      query: (taskId: string) => ({
        url: `/task/${taskId}`,
        method: 'DELETE'
      }),
      invalidatesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    assignedCanChange: builder.query({
      query: (taskId: number) => ({
        url: `/assigned/can_change/${taskId}`,
        method: 'GET'
      })
    }),
    editAssigned: builder.mutation({
      query: (params: { taskId: number, rate_type: string, rate: number, hours_spent: number }) => ({
        url: `/assigned/${params.taskId}`,
        method: 'PUT',
        body: {
          rate_type: params.rate_type,
          rate: params.rate,
          hours_spent: params.hours_spent
        }
      }),
      invalidatesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    assignedTask: builder.mutation({
      query: (params: { task: number, rate_type: string, rate: number, employee: number }) => ({
        url: '/assigned',
        method: 'POST',
        body: {
          task: params.task,
          rate_type: params.rate_type,
          rate: params.rate,
          employee: params.employee
        }
      }),
      invalidatesTags: [{ type: 'Task', id: 'LIST' }]
    }),
    createProjectManager: builder.mutation({
      query: (params: { project: number, employee: number, disabled: boolean }) => ({
        url: '/pm',
        method: 'POST',
        body: {
          project: params.project,
          employee: params.employee,
          disabled: params.disabled
        }
      })
    }),
    deleteProjectManager: builder.mutation({
      query: (employeeId: number) => ({
        url: `/pm/delete/${employeeId}`,
        method: 'DELETE'
      })
    }),
    getEmployeeMe: builder.query({
      query: (taskId: number) => ({
        url: `/employee/me/${taskId}`,
        method: 'GET'
      })
    })
  })
})

export const {
  useCreateTaskMutation,
  useSearchTaskQuery,
  useGetTaskQuery,
  useUpdateTaskMutation,
  useDeleteTaskMutation,
  useAssignedCanChangeQuery,
  useEditAssignedMutation,
  useAssignedTaskMutation,
  useCreateProjectManagerMutation,
  useDeleteProjectManagerMutation,
  useGetEmployeeMeQuery
} = TaskApi

export interface IKanbanColumns {
  [key: string]: {
    title: string
    items: ITask[]
  }
}

interface TaskState {
  tasks: ITask[]
  kanbanColumns: IKanbanColumns
  openModal: boolean
}

const initialState: TaskState = {
  tasks: [],
  kanbanColumns: {
    [EState.TODO]: {
      title: 'К виконанню',
      items: []
    },
    [EState.RESEARCH]: {
      title: 'В пошуці',
      items: []
    },
    [EState.IN_PROGRESS]: {
      title: 'В процессі',
      items: []
    },
    [EState.TESTING]: {
      title: 'Тестування',
      items: []
    },
    [EState.DONE]: {
      title: 'Завершено',
      items: []
    }
  },
  openModal: false
}

const taskSlice = createSlice({
  name: 'task',
  initialState,
  reducers: {
    setTaskState: (state, action: PayloadAction<ITask[]>) => {
      state.tasks = action.payload
    },
    setKanbanColumns: (state, action: PayloadAction<IKanbanColumns>) => {
      state.kanbanColumns = action.payload
    },
    setOpenModal: (state, action: PayloadAction<boolean>) => {
      state.openModal = action.payload
    }
  }
})

export const { setTaskState, setKanbanColumns, setOpenModal } = taskSlice.actions

export const selectTaskState = (state: RootState) => state?.task.tasks
export const selectKanbanColumns = (state: RootState) => state?.task.kanbanColumns
export const selectOpenModal = (state: RootState) => state?.task.openModal

export default taskSlice.reducer
