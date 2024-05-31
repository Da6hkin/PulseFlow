import React, { useEffect } from 'react'
import { Box, Button, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import { CompanyItem } from 'src/components/items/CompanyItem'
import CustomizedModal from 'src/components/CustomizedModal'
import CustomizedInput from 'src/components/CustomizedInput'
import { setCurrentCompany, useCreateCompanyMutation, useGetMeQuery, useSearchCompanyQuery } from 'src/store/company'
import { useDispatch, useSelector } from 'react-redux'
import { selectCurrentUserState } from 'src/store/users'
import { useCreateEmployeeMutation } from 'src/store/employee'

const CompanyPage: React.FC = () => {
  const dispatch = useDispatch()
  const { data } = useGetMeQuery()
  const [createCompany] = useCreateCompanyMutation()
  const [createEmployee] = useCreateEmployeeMutation()
  const currentUser = useSelector(selectCurrentUserState)
  const companies = useSearchCompanyQuery({ id: currentUser?.id })
  console.log(currentUser, companies)

  const [openModal, setOpenModal] = React.useState(false)
  const [nameCompany, setNameCompany] = React.useState('')
  const [idCompany, setIdCompany] = React.useState('')
  const [webCompany, setWebCompany] = React.useState('')

  useEffect(() => {
    data && dispatch(setCurrentCompany(data))
  }, [data])

  const handleOpenModal = () => {
    setOpenModal(true)
  }

  const handleCloseModal = () => {
    setOpenModal(false)
  }

  const handleCreateCompany = async () => {
    const formData = new FormData()
    formData.append('name', nameCompany)
    formData.append('unique_identifier', idCompany)
    formData.append('website', webCompany)
    await createCompany(formData).then(async (res: any) => {
      const data: any = {
        user: currentUser?.id,
        company: res?.id,
        is_project_manager: true,
        disabled: false
      }
      await createEmployee(data)
    })
    handleCloseModal()
  }

  const handleChangeCompany = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameCompany(e.target.value)
  }

  const handleChangeIdCompany = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIdCompany(e.target.value)
  }

  const handleChangeWebCompany = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWebCompany(e.target.value)
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
            Вітаємо
            на платформі PulseFlow
          </Typography>
          <Typography fontSize={20} >
            Тут ви можете долучитися до вже створеної компанії
            або додати та налаштувати власну.
          </Typography>
          <Typography fontSize={20} >
            Доступні компанії:
          </Typography>
          <Box
            width={'300px'}
            display={'flex'}
            flexDirection={'column'}
            justifyContent={'start'}
            alignItems={'start'}
            gap={'15px'}
          >
            <CompanyItem title={'Company 1'} />
            <CompanyItem title={'Company 2'} />
            <Button variant='contained' color='primary' sx={{
              width: '100%',
              marginTop: '20px'
            }}
            onClick={handleOpenModal}
            >
              Створити нову компанію
            </Button>
          </Box>
        </Box>
      </WrapperPage>
      {openModal && <CustomizedModal
        title={'Створення нової компанії'}
        handleClose={handleCloseModal}
        action={handleCreateCompany}
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
            value={nameCompany}
            onChange={handleChangeCompany}
            type='text'
            placeholder='Назва компанії' />

          <CustomizedInput
            value={idCompany}
            onChange={handleChangeIdCompany}
            type='text'
            placeholder='Унікальний ідентифікатор' />

          <CustomizedInput
            value={webCompany}
            onChange={handleChangeWebCompany}
            type='text'
            placeholder='Вебсайт' />
        </Box>
      </CustomizedModal>}
    </>
  )
}

export default CompanyPage
