import React from 'react'
import { Draggable } from 'react-beautiful-dnd'
import styled from '@emotion/styled'

const TaskInformation = styled.div`
  display: flex;
  cursor: pointer;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 0 15px;
  min-height: 150px;
  border-radius: 5px;
  max-width: 230px;
  min-width: 200px;
  background: rgba(255, 59, 59, 0.15);
  background: white;
  margin-top: 15px;

  .secondary-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    font-size: 12px;
    font-weight: 400px;
    color: #7d7d7d;
  }
`

export interface ITaskCard {
  item: {
    id: string
    task: string
    date: string
  }
  index: number
}

const TaskCard = ({ item, index }: ITaskCard) => {
  return (
    <Draggable key={item?.id} draggableId={item?.id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided?.draggableProps}
          {...provided?.dragHandleProps}
        >
          <TaskInformation>
            <p>{item?.task}</p>
            <div>
              <p>
                <span>
                  {new Date(item?.date).toLocaleDateString('en-us', {
                    month: 'short',
                    day: '2-digit'
                  })}
                </span>
              </p>
            </div>
          </TaskInformation>
        </div>
      )}
    </Draggable>
  )
}

export default TaskCard
