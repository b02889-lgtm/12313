# 获取当前时间的PowerShell脚本

Write-Host "=" * 50
Write-Host "当前时间信息"
Write-Host "=" * 50

# 获取当前时间
$now = Get-Date

# 格式化输出
Write-Host "完整时间: $($now.ToString('yyyy年MM月dd日 HH:mm:ss'))"
Write-Host "ISO格式: $($now.ToString('o'))"
Write-Host "星期: $($now.DayOfWeek)"
Write-Host "时间戳: $([int][double]::Parse((Get-Date -UFormat %s)))"
Write-Host "=" * 50

# 计算距离周末的时间
$currentDayOfWeek = [int]$now.DayOfWeek  # 0=周日, 1=周一, ..., 6=周六

Write-Host "`n距离周末（周六）还有："

if ($currentDayOfWeek -eq 6) {
    Write-Host "今天是周六！享受您的周末吧！"
} elseif ($currentDayOfWeek -eq 0) {
    Write-Host "今天是周日！享受您的周末吧！"
} else {
    # 计算到周六的天数
    if ($currentDayOfWeek -eq 0) {
        $daysUntilSaturday = 6
    } else {
        $daysUntilSaturday = 6 - $currentDayOfWeek
    }
    
    # 计算到今天午夜的时间
    $endOfToday = $now.Date.AddDays(1).AddSeconds(-1)
    $timeUntilMidnight = $endOfToday - $now
    
    # 计算总秒数
    $totalSeconds = $timeUntilMidnight.TotalSeconds + ($daysUntilSaturday - 1) * 24 * 3600
    
    # 转换为天时分秒
    $days = [math]::Floor($totalSeconds / (24 * 3600))
    $hours = [math]::Floor(($totalSeconds % (24 * 3600)) / 3600)
    $minutes = [math]::Floor(($totalSeconds % 3600) / 60)
    $seconds = [math]::Floor($totalSeconds % 60)
    
    Write-Host "天数: $days 天"
    Write-Host "小时: $hours 小时"
    Write-Host "分钟: $minutes 分钟"
    Write-Host "秒数: $seconds 秒"
    Write-Host "总分钟数: $($totalSeconds / 60) 分钟"
}