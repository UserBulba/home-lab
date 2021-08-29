### Make local machine.

# Prepare local machine to be a Vagrant host.
[Parameter()][string]$Share = "shared"

Push-Location -Path ..\

IF(!(Test-Path $Share))
{
    Try 
    {
        New-Item -Name $Share -Path (Get-Location) -ItemType "directory"
        Write-Host "Path - $Share - created" -ForegroundColor Yellow
    }
    Catch {Write-Warning $Error}
}
ELSE {Write-Host "`nPath - $Share - already exists`n" -ForegroundColor Green}

$Plugins = Invoke-Expression -Command "vagrant plugin list"

# Build vagrant.
IF(!$Plugins -match "vagrant-vbguest")
{Invoke-Expression -Command "vagrant plugin install vagrant-vbguest"}

Invoke-Expression -Command "vagrant up"

Invoke-Expression -Command "vagrant rsync-auto"

Pop-Location