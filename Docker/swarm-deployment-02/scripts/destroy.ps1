### Remove local machine.

# Stop vagrant.
Push-Location -Path ..\

Write-Host "`Stopping vagrant..." -ForegroundColor Yellow
Invoke-Expression -Command "vagrant halt"

Write-Host "`nDestroying vagrant..." -ForegroundColor Yellow
Invoke-Expression -Command "vagrant destroy --force"

Write-Host "`nStopping sync job..." -ForegroundColor Yellow
Get-Job | Stop-Job 
Get-Job | Remove-Job

Pop-Location
