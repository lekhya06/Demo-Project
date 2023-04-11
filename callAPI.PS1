$uri = "https://datausa.io/api/data?drilldowns=State&measures=Population"

Invoke-RestMethod -Uri $uri | 
Select-Object -ExpandProperty data |
Export-Csv data.csv -NoTypeInformation

Write-Output "Data saved to data.csv"