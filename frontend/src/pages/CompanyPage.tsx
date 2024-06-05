import React from 'react'
import { Box, Button, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
import { CompanyItem } from 'src/components/items/CompanyItem'
import CustomizedModal from 'src/components/CustomizedModal'
import CustomizedInput from 'src/components/CustomizedInput'
import StarIcon from '@mui/icons-material/Star'
import {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  ICompany, selectCurrentCompany, setCurrentCompany,
  useCreateCompanyMutation,
  useGetMeCompanyQuery
} from 'src/store/company'
import { useSelector, useDispatch } from 'react-redux'
import { useGetMeQuery } from 'src/store/users'
import { useCreateEmployeeMutation } from 'src/store/employee'

const CompanyPage: React.FC = () => {
  const dispatch = useDispatch()
  const [createCompany] = useCreateCompanyMutation()
  const [createEmployee] = useCreateEmployeeMutation()
  const { data: user } = useGetMeQuery()
  const { data: companyData, isLoading: isLoadingCompany } = useGetMeCompanyQuery()
  const getCompanies = useGetMeCompanyQuery().refetch
  const currentCompany = useSelector(selectCurrentCompany)

  const [openModal, setOpenModal] = React.useState(false)
  const [nameCompany, setNameCompany] = React.useState('')
  const [idCompany, setIdCompany] = React.useState('')
  const [webCompany, setWebCompany] = React.useState('')
  const [error, setError] = React.useState('')

  const handleOpenModal = () => {
    setOpenModal(true)
  }

  const handleCloseModal = () => {
    setOpenModal(false)
    setError('')
  }

  const handleCreateCompany = async () => {
    const data = {
      name: nameCompany,
      unique_identifier: idCompany,
      website: webCompany,
      creator: user?.id
    }
    await createCompany(data).then(async (res: any) => {
      if (res?.error) {
        setError('Помилка при створенні компанії')
      } else {
        const data: any = {
          user: user?.id,
          company: res?.data?.id,
          is_admin: true,
          disabled: false
        }
        setError('')
        await getCompanies()
        await createEmployee(data).then(() => {
          handleCloseModal()
        })
      }
    })
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

  const handleCurrentCompany = (company: ICompany) => {
    dispatch(setCurrentCompany(company))
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
            {!isLoadingCompany && companyData &&
              companyData?.length > 0 && companyData.map((company) => (
              <Box
                key={company?.id}
                display={'flex'}
                alignItems={'center'}
                gap={'15px'}
                onClick={() => handleCurrentCompany(company)}
              >
                <CompanyItem
                  title={company?.name}
                  subTitle={company?.unique_identifier}
                  info={company?.website ?? ''} />
                {(currentCompany?.id === company?.id) && <StarIcon style={{ width: '40px', height: '40px' }} />}
              </Box>
            ))}
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

export default CompanyPage
