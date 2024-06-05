import React from 'react'
import { Autocomplete, Box, Button } from '@mui/material'
import { useLocation } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectCurrentCompany } from 'src/store/company'
import CustomizedModal from './CustomizedModal'
import CustomizedInput from './CustomizedInput'
import { useCreateTaskMutation } from 'src/store/task'
import CustomizedDatePickers from './CustomizedDatePickers'
import { useProjectIsPmQuery } from 'src/store/project'
import { useEmployeeInvateMutation } from 'src/store/employee'

export const TaskPriorityOption = [
  { value: 1, title: 'Дуже низький' },
  { value: 2, title: 'Низький' },
  { value: 3, title: 'Середній' },
  { value: 4, title: 'Високий' },
  { value: 5, title: 'Дуже високий' }
]

export enum TaskPriority {
  'Дуже низький' = 1,
  'Низький',
  'Середній',
  'Високий',
  'Дуже високий'
}

interface IAddTasksModal {
  openModal: boolean
  handleClose: () => void
  getTasksRemoteState: () => void
}

const AddTasksModal = ({ openModal, handleClose, getTasksRemoteState }: IAddTasksModal) => {
  const location = useLocation()
  const [createTask] = useCreateTaskMutation()
  const [inviteEmployee] = useEmployeeInvateMutation()
  const projectId = location.pathname.split('/')[2]
  const currentCompany = useSelector(selectCurrentCompany)
  const { data: isProjectManager } = useProjectIsPmQuery(projectId)

  const [nameTask, setNameTask] = React.useState('')
  const [descriptionTask, setDescriptionTask] = React.useState('')
  const [priority, setPriority] = React.useState(5)
  const [startDate, setStartDate] = React.useState<Date>(new Date())
  const [endDate, setEndDate] = React.useState<Date | null>(null)
  const [searchEmail, setSearchEmail] = React.useState<string>('')
  const [modalMode, setModalMode] = React.useState<string>('begin')
  const [error, setError] = React.useState<string>('')

  const handleCloseModal = () => {
    setModalMode('begin')
    setDescriptionTask('')
    setNameTask('')
    setStartDate(new Date())
    setEndDate(null)
    setPriority(5)
    setSearchEmail('')
    handleClose()
    setError('')
  }

  const handleChangeNameTask = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameTask(e.target.value)
  }

  const handleChangeDescriptionTask = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescriptionTask(e.target.value)
  }

  const handleChangeStartDate = (date: Date) => {
    setStartDate(date)
  }

  const handleChangeEndDate = (date: Date) => {
    setEndDate(date)
  }

  const handleChangeEmployeeEmail = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchEmail(e.target.value)
  }

  const handleAddTaskMode = () => {
    setModalMode('task')
    setError('')
  }

  const handleAddEmployeeMode = () => {
    setModalMode('employee')
    setError('')
  }

  const handleCreateTask = async () => {
    const data: any = {
      state: 'todo',
      priority,
      name: nameTask,
      description: descriptionTask,
      planned_start_date: startDate,
      planned_end_date: endDate,
      project: projectId
    }
    await createTask(data).then((res: any) => {
      if (res?.error) {
        setError('Помилка при створенні задачі')
      } else {
        setError('')
        getTasksRemoteState()
        handleCloseModal()
      }
    }).catch((error: any) => {
      console.log('error', error)
    })
    setModalMode('begin')
  }

  const handleAddEmployee = async () => {
    await inviteEmployee({ email: searchEmail, company_id: Number(currentCompany?.id) }).then((res: any) => {
      if (res?.error) {
        setError('Користувача з таким імейлом не знайдено або він вже присутній у компанії')
      } else {
        setError('')
        handleCloseModal()
      }
    })
    setModalMode('begin')
  }

  return (
    <>
      {openModal && <CustomizedModal
        title={'Створення нової задачі'}
        handleClose={handleCloseModal}
        action={modalMode === 'task' ? handleCreateTask
          : modalMode === 'employee' ? handleAddEmployee : () => { return null }}
        open={openModal}
      >
        <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          justifyContent={'center'}
          gap={'15px'}
        >
          {modalMode === 'task' &&
            <>
              <CustomizedInput
                value={nameTask}
                onChange={handleChangeNameTask}
                type='text'
                placeholder='Назва задачі' />

              <CustomizedInput
                value={descriptionTask}
                onChange={handleChangeDescriptionTask}
                type='text'
                placeholder='Опис задачі' />

              <Autocomplete options={TaskPriorityOption}
                getOptionLabel={(option) => option.title}
                onChange={(e, newValue) => {
                  setPriority(newValue?.value ?? 5)
                }}
                sx={{
                  width: '381px',
                  height: '7px',
                  padding: '0 !important',
                  marginBottom: '37px'
                }}
                renderInput={(params) => <CustomizedInput {...params} />}
                value={TaskPriorityOption.find((option) => option.value === priority)}
              />

              <Box
                display={'flex'}
                alignItems={'center'}
                gap={'8px'}
              >
                <Box
                  display={'flex'}
                  flexDirection={'column'}
                  alignItems={'start'}
                >
                  <Box
                    color={'#000'}
                    fontSize={'14px'}
                    marginBottom={'5px'}
                    marginLeft={'7px'}
                  >
                      Дата початку
                  </Box>
                  <CustomizedDatePickers placeholder='Початкова дата' value={startDate} onChange={handleChangeStartDate} />
                </Box>
                <Box
                  display={'flex'}
                  flexDirection={'column'}
                  alignItems={'start'}
                >
                  <Box
                    color={'#000'}
                    fontSize={'14px'}
                    marginBottom={'5px'}
                    marginLeft={'7px'}
                  >
                      Дата закінчення
                  </Box>
                  <CustomizedDatePickers placeholder='Фінальна дата' value={endDate} onChange={handleChangeEndDate} />
                </Box>
              </Box>
            </>}
          {modalMode === 'employee' && isProjectManager &&
            <CustomizedInput
              value={searchEmail}
              onChange={handleChangeEmployeeEmail}
              type='text'
              placeholder='Імейл користувача' />}

          {modalMode === 'begin' &&
            <>
              <Button variant='contained' color='primary' sx={{
                width: '100%',
                marginTop: '20px'
              }}
              onClick={handleAddTaskMode}
              >
                Додати задачу
              </Button>
              {isProjectManager && <Button variant='contained' color='primary' sx={{
                width: '100%',
                marginTop: '20px'
              }}
              onClick={handleAddEmployeeMode}
              >
                Додати співробітника по імейлу
              </Button>}
            </>}
          {error && <Box sx={{
            color: 'red',
            fontSize: '14px'
          }}>
            {error}
          </Box>}
        </Box>
      </CustomizedModal>}
    </>
  )
}

export default AddTasksModal
