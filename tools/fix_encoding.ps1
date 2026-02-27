Get-ChildItem -Path "docs/systems/*.md" | ForEach-Object {
    $content = Get-Content $_.FullName
    $content | Out-File -FilePath $_.FullName -Encoding utf8
}
Write-Host "✅ Encodings corregidos a UTF-8." -ForegroundColor Green