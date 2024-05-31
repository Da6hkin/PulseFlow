import React from 'react'
import { Box, Button, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import { useNavigate } from 'react-router-dom'
import { CompanyItem } from 'src/components/items/CompanyItem'
import CustomizedModal from 'src/components/CustomizedModal'
import CustomizedInput from 'src/components/CustomizedInput'

const ProjectPage: React.FC = () => {
  const navigate = useNavigate()
  const [openModal, setOpenModal] = React.useState(false)
  const [namуProject, setNameProject] = React.useState('')
  const [description, setDescription] = React.useState('')

  const handleOpenModal = () => {
    setOpenModal(true)
  }

  const handleCloseModal = () => {
    setOpenModal(false)
  }

  const handleChangeProject = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameProject(e.target.value)
  }

  const handleChangeDescription = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDescription(e.target.value)
  }

  const handleCreateProject = () => {
    console.log('Create Project')
  }

  const handleClick = (id: string) => {
    navigate(`/task/${id}`)
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
            Проекти
          </Typography>
          <Typography fontSize={20} >
            Створюй свої проекти та долучайся до вже існуючих
          </Typography>
          <Typography fontSize={20} >
            Доступні проекти:
          </Typography>
          <Box
            width={'300px'}
            display={'flex'}
            flexDirection={'column'}
            justifyContent={'start'}
            alignItems={'start'}
            gap={'15px'}
          >
            <Box onClick={() => handleClick('1')}>
              <CompanyItem title={'Project 1'} />
            </Box>
            <Box onClick={() => handleClick('2')}>
              <CompanyItem title={'Project 2'} />
            </Box>
            <Button variant='contained' color='primary' sx={{
              width: '100%',
              marginTop: '20px'
            }}
            onClick={handleOpenModal}
            >
              Створити новий проект
            </Button>
          </Box>
        </Box>
      </WrapperPage>
      {openModal && <CustomizedModal
        title={'Створення нового проекту'}
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
            value={namуProject}
            onChange={handleChangeProject}
            type='text'
            placeholder='Назва проекту' />

          <CustomizedInput
            value={description}
            onChange={handleChangeDescription}
            type='text'
            placeholder='Опис проэкту' />

        </Box>
      </CustomizedModal>}
    </>
  )
}

export default ProjectPage
