### Remove local machine.

# Stop vagrant.
Push-Location -Path ..\

Write-Host "`nStoping vagrant..." -ForegroundColor Yellow
Invoke-Expression -Command "vagrant halt"
Write-Host "`nDestroying vagrant..." -ForegroundColor Yellow
Invoke-Expression -Command "vagrant destroy --force"

Pop-Location