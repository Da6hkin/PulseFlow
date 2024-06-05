/* eslint-disable no-void */
import React, { useEffect, useState } from 'react'
import styled from '@emotion/styled'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { DragDropContext, DropResult, Droppable } from 'react-beautiful-dnd'
import TaskCard from './TaskCard'
import { Autocomplete, Box, Button, InputAdornment } from '@mui/material'
import {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  IKanbanColumns, ITask,
  RateOptions,
  useAssignedTaskMutation,
  useUpdateTaskMutation
} from 'src/store/task'
import CustomizedInput from '../CustomizedInput'
import CustomizedModal from '../CustomizedModal'
import { serverURL } from 'src/config'
import axios from 'axios'
import { TaskPriority } from '../AddTasksModal'
import format from 'date-fns/format'
import AttachMoneyIcon from '@mui/icons-material/AttachMoney'

const Container = styled.div`
  display: flex;
`

const TaskList = styled.div`
  min-height: 100px;
  display: flex;
  flex-direction: column;
  background: #f3f3f3;
  max-width: 230px;
  min-width: 200px;
  border-radius: 5px;
  padding: 10px 10px 10px 0;
  margin-right: 5px;
`

const TaskColumnStyles = styled.div`
  margin: 8px;
  display: flex;
  width: 100%;
  min-height: 80vh;
`

const Title = styled.span`
  display: flex;
  align-items: center;
  width: 100%;
  color: #10957d;
  background: rgba(16, 149, 125, 0.15);
  padding: 2px 10px;
  border-radius: 5px;
  align-self: center;
`

type ISetColumns = (columns: IKanbanColumns) => void
interface IColumn {
  title: string
  items: Array<{
    id: string
    task: string
    date: string
  }>
}

const KanbanBoard = ({ kanbanColumns, handleGetTasksRemote }:
{ kanbanColumns: IKanbanColumns, handleGetTasksRemote: () => void }) => {
  const [updateTask] = useUpdateTaskMutation()
  const [assignedTask] = useAssignedTaskMutation()
  const [columns, setColumns] = useState(kanbanColumns)
  const [openModal, setOpenModal] = useState(false)
  const [taskAssign, setTaskAssign] = useState(null as ITask | null)
  const [isAssigned, setIsAssigned] = useState(false)
  const [salary, setSalary] = useState('fixed')
  const [sum, setSum] = useState('')
  const [quantity, setQuantity] = useState('')
  const [assignMode, setAssignMode] = useState(false)
  const [employee, setEmployee] = useState('')
  const [employeeMe, setEmployeeMe] = useState(null as any)

  const getAssignedCanChange = async (taskId: number) => {
    const token = localStorage.getItem('token') ?? ''
    await axios.get(`${serverURL}/api/assigned/can_change/${taskId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then((res) => {
      if (res?.data) {
        setIsAssigned(true)
      }
    }).catch(() => {
      setIsAssigned(false)
    })
  }

  const getEmployeeMe = async (taskId: number) => {
    const token = localStorage.getItem('token') ?? ''
    await axios.get(`${serverURL}/api/employee/me/${taskId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then((res: any) => {
      if (res?.data) {
        setEmployeeMe(res.data)
      }
    }).catch(() => {
      console.log('error')
    })
  }

  const handleChangeHour = () => {
    if (isAssigned && (taskAssign?.assigned?.length > 0)) {
      void handleUpdateAssignTask().then(() => {
        handleGetTasksRemote()
      })
    }
  }

  useEffect(() => {
    if (taskAssign?.hours_spent) {
      (taskAssign?.hours_spent >= 0) && setQuantity(taskAssign?.hours_spent.toString())
    }
  }, [taskAssign])

  useEffect(() => {
    if (taskAssign?.assigned?.length > 0) {
      const userObj = taskAssign?.assigned[0]?.employee?.user
      // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
      const user = `${userObj?.name}  ${userObj?.surname} / ${userObj?.email}`
      setEmployee(user)
    }
  }, [taskAssign])

  useEffect(() => {
    if (taskAssign?.id) {
      void getEmployeeMe(taskAssign?.id)
    }
  }, [taskAssign])

  const handleOpenModal = () => {
    setOpenModal(true)
  }

  const handleAssignMode = () => {
    setAssignMode(true)
  }

  const handleCloseModal = () => {
    setOpenModal(false)
    setSum('')
    setQuantity('')
    setAssignMode(false)
    setEmployee('')
    setEmployeeMe(null)
  }

  const handleChangeTask = (task: ITask) => {
    setTaskAssign(task)
    void getAssignedCanChange(task?.id)
  }

  async function handleUpdateAssignTask () {
    if (taskAssign?.id) {
      await updateTask({
        taskId: taskAssign?.id,
        task: {
          ...taskAssign,
          hours_spent: Number(quantity)
        }
      }).then(() => {
        handleCloseModal()
      })
    }
  }

  const handleAssignTask = async () => {
    await assignedTask({
      task: taskAssign ? taskAssign?.id : 0,
      rate_type: salary,
      rate: Number(sum),
      employee: employeeMe?.id
    }).then(() => {
      handleGetTasksRemote()
      handleCloseModal()
    })
  }

  const handleChangeSum = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSum(e.target.value)
  }

  const handleChangeQuantity = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuantity(e.target.value)
  }

  const handleUpdateTask = async (task: ITask, state: string) => {
    const newTask = { ...task, state }
    await updateTask({
      task: newTask,
      taskId: task?.id
    })
  }

  const onDragEnd = (result: DropResult, columns: IKanbanColumns, setColumns: ISetColumns) => {
    if (!result?.destination) return
    const { source, destination } = result
    if (source?.droppableId !== destination?.droppableId) {
      const sourceColumn = columns[source?.droppableId]
      const destColumn = columns[destination?.droppableId]
      const sourceItems = [...sourceColumn?.items]
      const destItems = [...destColumn?.items]
      const [removed] = sourceItems?.splice(source?.index, 1)
      destItems?.splice(destination.index, 0, removed)
      void handleUpdateTask(removed, destination.droppableId)
      setColumns({
        ...columns,
        [source.droppableId]: {
          ...sourceColumn,
          items: sourceItems
        },
        [destination.droppableId]: {
          ...destColumn,
          items: destItems
        }
      })
    } else {
      const column = columns[source.droppableId]
      const copiedItems = [...column.items]
      const [removed] = copiedItems?.splice(source.index, 1)
      copiedItems?.splice(destination.index, 0, removed)
      setColumns({
        ...columns,
        [source?.droppableId]: {
          ...column,
          items: copiedItems
        }
      })
    }
  }
  return (
    <>
      <Box
        width={'50wh'}
      >
        <DragDropContext
          onDragEnd={(result: DropResult) => onDragEnd(result, columns, setColumns)}
        >
          <Container>
            <TaskColumnStyles>
              {Object.entries(columns).map(([columnId, column]: any, index) => {
                return (
                  <Droppable key={columnId} droppableId={columnId}>
                    {(provided, snapshot) => (
                      <TaskList
                        ref={provided.innerRef}
                        {...provided.droppableProps}
                      >
                        <Title>{column.title}</Title>
                        {column?.items?.map((item: any, index: number) => (
                          <Box
                            key={item?.id}
                            onClick={() => {
                              handleOpenModal()
                              handleChangeTask(item)
                            }}
                          >
                            <TaskCard item={item} index={index} />
                          </Box>
                        ))}
                        {provided.placeholder}
                      </TaskList>
                    )}
                  </Droppable>
                )
              })}
            </TaskColumnStyles>
          </Container>
        </DragDropContext>
      </Box>
      {openModal && <CustomizedModal
        title={(isAssigned && !(taskAssign?.assigned?.length > 0)) ? 'Доєднатись до завдання' : 'Редагувати години'}
        handleClose={handleCloseModal}
        action={(isAssigned && !(taskAssign?.assigned?.length > 0)) ? handleAssignTask : () => { return null }}
        open={openModal}
      >
        {!assignMode && <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          justifyContent={'center'}
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
              marginLeft={'7px'}
            >
              Назва задачі
            </Box>
            <CustomizedInput
              value={taskAssign?.name}
              type='text'
              disabled />
          </Box>

          {isAssigned && <Box
            display={'flex'}
            flexDirection={'column'}
            alignItems={'start'}
          >
            <Box
              color={'#000'}
              fontSize={'14px'}
              marginLeft={'7px'}
            >
              Кількість годин
            </Box>
            <CustomizedInput
              value={quantity}
              onChange={handleChangeQuantity}
              type='number'
              placeholder='Кількість годин' />
          </Box>}

          <Box
            display={'flex'}
            flexDirection={'column'}
            alignItems={'start'}
          >
            <Box
              color={'#000'}
              fontSize={'14px'}
              marginLeft={'7px'}
            >
              Пріоритетність
            </Box>
            <CustomizedInput
              value={TaskPriority[taskAssign?.priority ?? 1]}
              type='text'
              disabled />
          </Box>

          <Box
            display={'flex'}
            flexDirection={'column'}
            alignItems={'start'}
          >
            <Box
              color={'#000'}
              fontSize={'14px'}
              marginLeft={'7px'}
            >
              Дата початку
            </Box>
            <CustomizedInput
              value={format(new Date(taskAssign?.planned_start_date ?? ''), 'dd-MM-yyyy')}
              type='text'
              disabled
            />
          </Box>
          <Box
            display={'flex'}
            flexDirection={'column'}
            alignItems={'start'}
          >
            <Box
              color={'#000'}
              fontSize={'14px'}
              marginLeft={'7px'}
            >
              Дата закінчення
            </Box>
            <CustomizedInput
              value={format(new Date(taskAssign?.planned_end_date ?? ''), 'dd-MM-yyyy')}
              type='text'
              disabled
            />
          </Box>

          <Box
            display={'flex'}
            flexDirection={'column'}
            alignItems={'center'}
            gap={'15px'}
          >
            <Box
              color={'#000'}
              fontSize={'14px'}
              marginLeft={'7px'}
            >
              Виконавець: {employee ? `${employee}` : undefined}
            </Box>
            {!(taskAssign?.assigned?.length > 0) && <Button
              onClick={handleAssignMode}
              variant={'contained'}
              color={'primary'}
              sx={{
                width: '380px'
              }}
            >
            Додатись як виконавець
            </Button>}
            {(taskAssign?.assigned?.length > 0) && isAssigned && <Button
              onClick={handleChangeHour}
              variant={'contained'}
              color={'primary'}
              sx={{
                width: '380px'
              }}
            >
                Оновити години
            </Button>}
          </Box>
        </Box>}

        {assignMode && <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          justifyContent={'center'}
          gap={'15px'}
        >

          <Autocomplete options={RateOptions}
            getOptionLabel={(option) => option.title}
            onChange={(e, newValue) => {
              setSalary(newValue?.value ?? 'fixed')
            }}
            sx={{
              width: '381px',
              height: '7px',
              padding: '0 !important',
              marginBottom: '37px'
            }}
            renderInput={(params) => <CustomizedInput {...params} />}
            value={RateOptions.find((option) => option.value === salary)}
          />

          <CustomizedInput
            value={sum}
            onChange={handleChangeSum}
            type='number'
            placeholder='Cума $'
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <AttachMoneyIcon />
                </InputAdornment>
              )
            }} />

        </Box>}
      </CustomizedModal>}
    </>
  )
}

export default KanbanBoard
