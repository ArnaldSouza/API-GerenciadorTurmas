$PYTHON_EXEC = ".\\.venv\\Scripts\\python.exe"

Write-Host "🚀 EXECUTANDO TESTES" -ForegroundColor Green

# Iniciar Django
$djangoProcess = Start-Process -FilePath $PYTHON_EXEC -ArgumentList "manage.py", "runserver", "8000" -PassThru -NoNewWindow
Start-Sleep 5

# Executar testes
try {
    & $PYTHON_EXEC "test_complete.py"
    Write-Host "✓ Testes REST concluídos!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro nos testes: $_" -ForegroundColor Red
}

# Testar gRPC se existir
if (Test-Path "grpc") {
    Set-Location grpc
    $grpcProcess = Start-Process -FilePath $PYTHON_EXEC -ArgumentList "gerenciador_grpc_server.py" -PassThru -NoNewWindow
    Start-Sleep 3
    Set-Location ..
    
    try {
        & $PYTHON_EXEC "test_grpc.py"
        Write-Host "✓ Testes gRPC concluídos!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Erro nos testes gRPC: $_" -ForegroundColor Red
    }
    
    if ($grpcProcess -and -not $grpcProcess.HasExited) {
        Stop-Process $grpcProcess.Id -Force
    }
}

# Parar Django
if ($djangoProcess -and -not $djangoProcess.HasExited) {
    Stop-Process $djangoProcess.Id -Force
}

Write-Host "🎉 TESTES CONCLUÍDOS!" -ForegroundColor Green