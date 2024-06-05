import React, { useEffect } from 'react'
import { Box, Button, InputAdornment, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import { useNavigate } from 'react-router-dom'
import { CompanyItem } from 'src/components/items/CompanyItem'
import CustomizedModal from 'src/components/CustomizedModal'
import CustomizedInput from 'src/components/CustomizedInput'
import { useSelector, useDispatch } from 'react-redux'
import { selectCurrentCompany } from 'src/store/company'
import { setProjectState, useCreateProjectMutation, useSearchProjectQuery } from 'src/store/project'
import { formatDate } from 'src/components/utils/formatDate'
import CustomizedDatePickers from 'src/components/CustomizedDatePickers'
import AttachMoneyIcon from '@mui/icons-material/AttachMoney'

const ProjectPage: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const currentCompany = useSelector(selectCurrentCompany)
  const { data: allProjects, isLoading } = useSearchProjectQuery({ company: currentCompany?.id })
  const getAllProjects = useSearchProjectQuery({ company: currentCompany?.id }).refetch
  const [createProject] = useCreateProjectMutation()

  const [openModal, setOpenModal] = React.useState(false)
  const [nameProject, setNameProject] = React.useState('')
  const [description, setDescription] = React.useState('')
  const [startDate, setStartDate] = React.useState<Date>(new Date())
  const [endDate, setEndDate] = React.useState<Date | null>(null)
  const [income, setIncome] = React.useState<number>()
  const [error, setError] = React.useState('')

  useEffect(() => {
    allProjects && dispatch(setProjectState(allProjects))
  }, [allProjects, currentCompany])

  const handleOpenModal = () => {
    setOpenModal(true)
  }

  const handleCloseModal = () => {
    setOpenModal(false)
    setError('')
  }

  const handleChangeProject = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameProject(e.target.value)
  }

  const handleChangeDescription = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescription(e.target.value)
  }

  const handleCreateProject = async () => {
    currentCompany && await createProject({
      name: nameProject,
      description,
      company: currentCompany.id,
      start_date: startDate,
      end_date: endDate ?? undefined,
      income
    })
      .then(async (res: any) => {
        if (res?.error) {
          setError('Помилка при створенні проєкту')
        } else {
          setError('')
          await getAllProjects()
          handleCloseModal()
        }
      })
  }

  const handleClick = (id: number) => {
    navigate(`/task/${id}`)
  }

  const handleChangeStartDate = (date: Date) => {
    setStartDate(date)
  }

  const handleChangeEndDate = (date: Date) => {
    setEndDate(date)
  }

  const handleChangeIncome = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIncome(Number(e.target.value))
  }

  return (
    <>
      <WrapperPage>
        <Box
          display={'flex'}
          flexDirection={'column'}
          justifyContent={'start'}
          alignItems={'start'}
          gap={'30px'}
        >
          <Typography fontSize={30} >
            Проєкти
          </Typography>
          {currentCompany
            ? <>
              <Typography fontSize={20} >
                Створюй свої проєкти та долучайся до вже існуючих
              </Typography>
              <Typography fontSize={20} >
                Доступні проєкти:
              </Typography>
            </>
            : <Typography fontSize={20} >
              Для створення проєктів потрібно обрати компанію
            </Typography>}
          {currentCompany && <Box
            width={'300px'}
            display={'flex'}
            flexDirection={'column'}
            justifyContent={'start'}
            alignItems={'start'}
            gap={'15px'}
          >
            {!isLoading && allProjects &&
              allProjects?.length > 0 && allProjects.map((project) => {
              const date = formatDate(project?.start_date).format2
              return (<Box
                key={project?.id}
                display={'flex'}
                alignItems={'center'}
                gap={'15px'}
                onClick={() => handleClick(project.id)}
              >
                <CompanyItem
                  title={project?.name}
                  subTitle={project?.description}
                  info={date} />
              </Box>)
            })}
            <Button variant='contained' color='primary' sx={{
              width: '100%',
              marginTop: '20px'
            }}
            onClick={handleOpenModal}
            >
              Створити новий проєкт
            </Button>
          </Box>}
        </Box>
      </WrapperPage>
      {openModal && <CustomizedModal
        title={'Створення нового проєкту'}
        handleClose={handleCloseModal}
        action={handleCreateProject}
        open={openModal}
      >
        <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          justifyContent={'center'}
          gap={'15px'}
        >
          <CustomizedInput
            value={nameProject}
            onChange={handleChangeProject}
            type='text'
            placeholder='Назва проєкту' />

          <CustomizedInput
            value={description}
            onChange={handleChangeDescription}
            type='text'
            placeholder='Опис проэкту' />

          <CustomizedInput
            value={income}
            onChange={handleChangeIncome}
            type='number'
            placeholder='Дохід $'
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <AttachMoneyIcon />
                </InputAdornment>
              )
            }}
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

export default ProjectPage
