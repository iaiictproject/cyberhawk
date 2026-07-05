param(
    [Parameter(Mandatory=$true)]
    [string]$Target,
    [switch]$SubsOnly
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    CyberHawk Recon - Professional Reconnaissance Tool" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

if ($SubsOnly) {
    python cyberhawk.py -t $Target --no-ports
} else {
    python cyberhawk.py -t $Target
}
