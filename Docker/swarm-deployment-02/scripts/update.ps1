### Update vagrant plugins.

# Stop vagrant.
Push-Location -Path ..\

$Plugins = Invoke-Expression -Command "vagrant plugin list"
ForEach($Plugin in $Plugins)
    {   
        $Plugin = $Plugin.Split("")[0]
        Invoke-Expression -Command "vagrant plugin update $Plugin"
    }

Pop-Location