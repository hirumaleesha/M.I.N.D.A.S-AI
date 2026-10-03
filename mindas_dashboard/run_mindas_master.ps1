# =====================================================================
# M.I.N.D.A.S. - Metacognitive Observer & Shared Memory Engine
# Master Cross-Language Orchestrator & Launch Automation Script
# =====================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🧠 M.I.N.D.A.S. System Core Orchestrator Launching... " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# ---------------------------------------------------------------------
# Step 1: Rust Core Shared Memory DLL Compilation
# ---------------------------------------------------------------------
Write-Host "`n[Step 1/4] Compiling Rust Dynamic Memory Bridge (mindas_core.dll)..." -ForegroundColor Yellow

$RustDir = Join-Path -Path$PSScriptRoot -ChildPath "mindas_core_rust"

if (Test-Path $RustDir) {
    Set-Location $RustDir
    cargo build --release
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ [ERROR] Rust Compilation Failed! Exiting process." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "✅ [SUCCESS] Rust DLL built successfully at target/release/mindas_core.dll" -ForegroundColor Green
    Set-Location $PSScriptRoot
} else {
    Write-Host "⚠️ [WARNING] Rust directory '$RustDir' not found! Skipping build step..." -ForegroundColor Red
}

# ---------------------------------------------------------------------
# Step 2: Launching Julia Theory of Mind (ToM) Engine in Parallel
# ---------------------------------------------------------------------
Write-Host "`n[Step 2/4] Launching Julia Theory of Mind Engine (tom_engine.jl)..." -ForegroundColor Yellow

$JuliaScript = Join-Path -Path $PSScriptRoot -ChildPath "mindas_tom_julia/tom_engine.jl"

if (Test-Path $JuliaScript) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '--- JULIA ToM ENGINE LOGS ---' -ForegroundColor Magenta; julia '$JuliaScript'"
    Write-Host "✅ [LAUNCHED] Julia ToM Engine background worker started." -ForegroundColor Green
} else {
    Write-Host "⚠️ [WARNING] Julia script '$JuliaScript' not found!" -ForegroundColor Red
}

# ---------------------------------------------------------------------
# Step 3: Launching Mojo Brain Tensor Engine
# ---------------------------------------------------------------------
Write-Host "`n[Step 3/4] Launching Mojo Tensor Brain Engine (brain.mojo)..." -ForegroundColor Yellow

$MojoScript = Join-Path -Path$PSScriptRoot -ChildPath "mindas_brain_mojo/brain.mojo"

if (Test-Path $MojoScript) {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '--- MOJO BRAIN ENGINE LOGS ---' -ForegroundColor Cyan; mojo '$MojoScript'"
    Write-Host "✅ [LAUNCHED] Mojo Brain Execution Engine started." -ForegroundColor Green
} else {
    Write-Host "⚠️ [WARNING] Mojo script '$MojoScript' not found!" -ForegroundColor Red
}

# ---------------------------------------------------------------------
# Step 4: Launching Streamlit Metacognitive Dashboard
# ---------------------------------------------------------------------
Write-Host "`n[Step 4/4] Starting Metacognitive Observer UI Dashboard..." -ForegroundColor Yellow

$DashboardDir = Join-Path -Path $PSScriptRoot -ChildPath "mindas_dashboard"

if (Test-Path $DashboardDir) {
    Set-Location $DashboardDir
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '--- STREAMLIT DASHBOARD LOGS ---' -ForegroundColor Yellow; streamlit run app.py"
    Write-Host "✅ [LAUNCHED] Streamlit UI Dashboard hosted on http://localhost:8501" -ForegroundColor Green
    Set-Location $PSScriptRoot
} else {
    Write-Host "⚠️ [WARNING] Dashboard directory '$DashboardDir' not found!" -ForegroundColor Red
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " 🚀 All M.I.N.D.A.S. Modules Successfully Orchestrated! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan