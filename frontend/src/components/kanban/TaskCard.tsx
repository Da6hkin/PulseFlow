import React from 'react'
import { Draggable } from 'react-beautiful-dnd'
import styled from '@emotion/styled'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { ITask } from 'src/store/task'
import { formatDate } from '../utils/formatDate'
import { TaskPriority } from '../AddTasksModal'

const TaskInformation = styled.div`
  display: flex;
  cursor: pointer;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px;
  min-height: 150px;
  border-radius: 10px;
  max-width: 230px;
  min-width: 200px;
  background: rgba(255, 59, 59, 0.15);
  background: white;
  margin-top: 15px;
  border: 1px solid #e0e0e0;
  gap: 5px;

  .secondary-details {
    max-width: 180px;
    min-height: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    overflow: hidden;
    word-wrap: break-word;
    font-size: 12px;
    font-weight: 400px;
    color: #7d7d7d;
  }
`

export interface ITaskCard {
  item: ITask
  index: number
}

const TaskCard = ({ item, index }: ITaskCard) => {
  return (
    <Draggable key={item?.id} draggableId={item?.id.toString()} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided?.draggableProps}
          {...provided?.dragHandleProps}
        >
          <TaskInformation>
            <div className='secondary-details'>{item?.name}</div>
            <div className='secondary-details'>{item?.description}</div>
            <div className='secondary-details'>Пріоритет: {TaskPriority[item?.priority]}</div>
            <div className='secondary-details'>
              {formatDate(item?.planned_start_date).format2}
            </div>
            <div className='secondary-details'>
              {formatDate(item?.planned_end_date).format2}
            </div>
          </TaskInformation>
        </div>
      )}
    </Draggable>
  )
}

export default TaskCard
