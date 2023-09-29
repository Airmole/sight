export const time = {
    timeStringFilename(timestamp = 0) {
        if (timestamp !== 0 && timestamp.toString().length === 10) timestamp = timestamp * 1000
        const date = timestamp === 0 ? new Date() : new Date(timestamp)
        const Y = date.getFullYear()
        const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
        const D = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate())
        const h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours())
        const m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes())
        const s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
        return `${Y}-${M}-${D}_${h}_${m}_${s}`
    }
}
