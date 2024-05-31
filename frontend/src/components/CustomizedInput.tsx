import { TextField, styled } from '@mui/material'

const CustomizedInput = styled(TextField)(`
.MuiInputBase-input{
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.15px;
  outline: none;
  padding: 2px 4px;
  &::placeholder {
    font-size: 16px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
  }
}
.MuiOutlinedInput-root {
  width: 381px;
  height: 40px;
  border-radius: 16px;
  border-color: rgba(65, 65, 213, 0.30);
  input {
    padding-left: 16px;
  }
}
.MuiOutlinedInput-notchedOutline {
  border-radius: 16px;
  border-color: rgba(65, 65, 213, 0.30);
}
`)
export default CustomizedInput
