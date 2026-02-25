// 获取当前时间的JavaScript脚本

function getCurrentTime() {
    const now = new Date();
    
    console.log("=".repeat(50));
    console.log("当前时间信息");
    console.log("=".repeat(50));
    console.log(`完整时间: ${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`);
    console.log(`ISO格式: ${now.toISOString()}`);
    console.log(`星期: ${['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()]}`);
    console.log(`时间戳: ${now.getTime()}`);
    console.log("=".repeat(50));
    
    return now;
}

function getTimeUntilWeekend() {
    const now = new Date();
    const currentDayOfWeek = now.getDay(); // 0=周日, 1=周一, ..., 6=周六
    
    console.log("\n距离周末（周六）还有：");
    
    if (currentDayOfWeek === 6) {
        console.log("今天是周六！享受您的周末吧！");
    } else if (currentDayOfWeek === 0) {
        console.log("今天是周日！享受您的周末吧！");
    } else {
        // 计算到周六的天数
        const daysUntilSaturday = 6 - currentDayOfWeek;
        
        // 计算到今天午夜的时间
        const endOfToday = new Date(now);
        endOfToday.setHours(23, 59, 59, 999);
        const timeUntilMidnight = endOfToday - now;
        
        // 计算总毫秒数
        const totalMilliseconds = timeUntilMidnight + (daysUntilSaturday - 1) * 24 * 60 * 60 * 1000;
        
        // 转换为天时分秒
        const days = Math.floor(totalMilliseconds / (24 * 60 * 60 * 1000));
        const hours = Math.floor((totalMilliseconds % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
        const minutes = Math.floor((totalMilliseconds % (60 * 60 * 1000)) / (60 * 1000));
        const seconds = Math.floor((totalMilliseconds % (60 * 1000)) / 1000);
        
        console.log(`天数: ${days} 天`);
        console.log(`小时: ${hours} 小时`);
        console.log(`分钟: ${minutes} 分钟`);
        console.log(`秒数: ${seconds} 秒`);
        console.log(`总分钟数: ${(totalMilliseconds / (60 * 1000)).toFixed(2)} 分钟`);
    }
}

// 执行函数
getCurrentTime();
getTimeUntilWeekend();