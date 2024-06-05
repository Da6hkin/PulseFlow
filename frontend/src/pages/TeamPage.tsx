import React from 'react'
import { Box, Typography } from '@mui/material'
import WrapperPage from 'src/components/WrapperPage'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { IEmployee, useGetEmployeeByCompanyQuery } from 'src/store/employee'
import { useSelector } from 'react-redux'
import { selectCurrentCompany } from 'src/store/company'
import { CompanyItem } from 'src/components/items/CompanyItem'
import CustomizedModal from 'src/components/CustomizedModal'
import { useGetMeQuery } from 'src/store/users'
import { useLocation } from 'react-router-dom'
import { useCreateProjectManagerMutation, useDeleteProjectManagerMutation } from 'src/store/task'

const TeamPage: React.FC = () => {
  const { data: user } = useGetMeQuery()
  const currentCompany = useSelector(selectCurrentCompany)
  const projectId = useLocation().pathname.split('/')[2]
  const team = currentCompany && useGetEmployeeByCompanyQuery(currentCompany?.id)?.data
  const refetchTeam = useGetEmployeeByCompanyQuery(currentCompany?.id ?? 0).refetch
  const [createPM] = useCreateProjectManagerMutation()
  const [deletePM] = useDeleteProjectManagerMutation()

  const [changedUser, setChangedUser] = React.useState<IEmployee | null>(null)
  const [isLoading, setIsLoading] = React.useState(false)
  const isAdmin = team?.filter((employee: IEmployee) => employee?.user?.id === user?.id)[0]?.is_admin
  const isPm = changedUser?.project_manager === true

  const handleCloseModal = () => {
    setChangedUser(null)
  }

  const handleOpenModal = (user: IEmployee) => {
    setChangedUser(user)
  }

  const handleChangeUser = async () => {
    setIsLoading(true)
    if (isPm && changedUser?.id) {
      await deletePM(changedUser?.id)
    } else if (changedUser?.id) {
      await createPM({ project: Number(projectId), employee: changedUser?.id, disabled: false })
    }
    await refetchTeam()
    setChangedUser(null)
    handleCloseModal()
    setIsLoading(false)
  }

  return (
    <>
      <WrapperPage>
        <Box
          display={'flex'}
          alignItems={'start'}
          justifyContent={'space-between'}
          flexDirection={'column'}
          gap={'15px'}>
          <Typography fontSize={30} paddingBottom={'15px'}>
            {currentCompany ? 'Команда' : 'Ви не обрали компанію, щоб переглянути команду'}
          </Typography>
          {!isLoading && team && team?.length > 0 && team.map((user: IEmployee) => (
            <Box
              key={user?.id}
              onClick={() => isAdmin && handleOpenModal(user)}
            >
              <CompanyItem
                teamMode
                title={user?.user?.name}
                subTitle={user?.user?.surname}
                info={user?.user?.email}
                isAdmin={user?.is_admin}
                isPm={user?.project_manager === true}
                isDeveloper={user?.project_manager === false}
              />
            </Box>
          ))}
        </Box>
      </WrapperPage>
      {!!changedUser && <CustomizedModal
        title={'Змінити користувача'}
        handleClose={handleCloseModal}
        action={isAdmin ? handleChangeUser : () => { return null }}
        open={!!changedUser}
      >
        <Box
          display={'flex'}
          flexDirection={'column'}
          alignItems={'center'}
          justifyContent={'center'}
          gap={'15px'}
        >
          <Typography>{`Ви змінюєте користувача ${changedUser?.user?.email} с проджект менеджера на розробника та навпаки`}</Typography>
        </Box>
      </CustomizedModal>}
    </>
  )
}

export default TeamPage
