export default {
    generate(data) {
        data.forEach((e, index) => {
            e.duration =  e.end - e.start
            e.level = index
        })
        data.sort((a,b) => b.duration - a.duration)
        data.forEach(e => e.position = e.level)
    }
}
