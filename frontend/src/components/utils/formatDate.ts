export function formatDate (dateString: string) {
  const date = new Date(dateString)
  const day = date?.getDate().toString().padStart(2, '0')
  const monthIndex = date?.getMonth() // 0-11
  const year = date?.getFullYear()

  const ukrainianMonths = [
    'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
    'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
  ]

  const monthName = ukrainianMonths[monthIndex]
  const formattedDate1 = `${day} / ${monthIndex + 1}`.padStart(2, '0')
  const formattedDate2 = `${day} / ${monthName} / ${year}`

  return {
    format1: formattedDate1,
    format2: formattedDate2
  }
}
