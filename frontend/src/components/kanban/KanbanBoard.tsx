import React, { useState } from 'react'
import styled from '@emotion/styled'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { DragDropContext, DropResult, Droppable } from 'react-beautiful-dnd'
import TaskCard from './TaskCard'
import { IKanbanColumns, kanbanColumns } from './kanbanData'
import { Box } from '@mui/material'

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
  padding: 10px 10px;
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

const KanbanBoard = () => {
  const [columns, setColumns] = useState(kanbanColumns)

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
    <Box
      width={'50wh'}
    >
      <DragDropContext
        onDragEnd={(result: DropResult) => onDragEnd(result, columns, setColumns)}
      >
        <Container>
          <TaskColumnStyles>
            {Object.entries(columns).map(([columnId, column], index) => {
              return (
                <Droppable key={columnId} droppableId={columnId}>
                  {(provided, snapshot) => (
                    <TaskList
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                    >
                      <Title>{column.title}</Title>
                      {column.items.map((item, index) => (
                        <Box
                          key={item?.id}
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
  )
}

export default KanbanBoard
