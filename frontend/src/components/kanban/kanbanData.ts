export interface IKanbanData {
  id: string
  task: string
  date: string
}

export const kanbanData: IKanbanData[] = [
  {
    id: '1',
    task: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent.',
    date: '25-May-2020'
  },
  {
    id: '2',
    task: 'Fix Styling',
    date: '26-May-2020'
  },
  {
    id: '3',
    task: 'Handle Door Specs',
    date: '27-May-2020'
  },
  {
    id: '4',
    task: 'morbi',
    date: '23-Aug-2020'
  },
  {
    id: '5',
    task: 'proin',
    date: '05-Jan-2021'
  }
]

export interface IKanbanColumns {
  [key: string]: {
    title: string
    items: IKanbanData[]
  }
}

export const kanbanColumns: IKanbanColumns = {
  toDo: {
    title: 'To-do',
    items: kanbanData
  },
  inProgress: {
    title: 'In Progress',
    items: []
  },
  testing: {
    title: 'Testing',
    items: []
  },
  ready: {
    title: 'Ready',
    items: []
  },
  done: {
    title: 'Done',
    items: []
  }
}
