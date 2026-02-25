$pythonPath = "C:\Users\v-haoguoliang\AppData\Local\Programs\Python\Python313\"
$scriptsPath = "C:\Users\v-haoguoliang\AppData\Local\Programs\Python\Python313\Scripts\"

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*$pythonPath*") {
    $newPath = "$pythonPath;$scriptsPath;$currentPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Python added to PATH" -ForegroundColor Green
    Write-Host "Please restart terminal to apply changes" -ForegroundColor Yellow
} else {
    Write-Host "Python already in PATH" -ForegroundColor Cyan
}