$PORT = 5000
Write-Host "Port: $PORT"

$body = @{
   CHAS = @{ "0" = 0 }
   RM = @{ "0" = 6.575 }
   TAX = @{ "0" = 296.0 }
   PTRATIO = @{ "0" = 15.3 }
   B = @{ "0" = 396.9 }
   LSTAT = @{ "0" = 4.98 }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:$PORT/predict -Method POST -Body $body -ContentType "application/json"
