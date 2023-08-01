import * as timers from "timers";

function solution(queries) {
    const memoryDB = [] // { id: string, entry:object, timestamp: number }
    const setEntry = (query, db) => {

        const [command, timestamp, key, field, value] = query
        // Check DB to see if the key exists.
        let record = db.find((r) => r.id === key)
        if(!record){
            record = { timestamp: timestamp, id: key, entry: {}}
            record.entry[field] = {
                value: value,
                timestamp: timestamp,
                ttl: 0
            }
            db.push(record)
            return ""
        }
        record.entry[field] = value
        return ""
    }
const compareAndSetEntry = (query, db) => {
    const [command, timestamp, key, field, expectedValue, newValue] = query
// Check DB to see if the key exists.
    let record = db.find((r) => r.id === key)
    if(!record){
        return "false"
    }
    if(record.entry[field] && record.entry[field] === expectedValue){
        record.entry[field] = newValue
        return "true"
    }
    return "false"
}
const compareAndDelete = (query, db) => {
    const [command, timestamp, key, field, expectedValue] = query
    let record = db.find((r) => r.id === key)
    if(record && record.entry[field] && record.entry[field] === expectedValue){
        delete record.entry[field]
        return "true"
    }
    return "false"
}
const getEntry = (query, db) => {
    const [command, timestamp, key, field] = query
    let record = db.find((r) => r.id === key)
    if(record && record.entry[field]) {
        if(!record.entry[field].tll){
            return record.entry[field]
        }
        if(timestamp >= record.timestamp && timestamp < record.entry[field].ttl) {
            return record.entry[field]
        }
    }
    return ""
}
const scanEntry = (query, db) => {
    [command, timestamp, key] = query
    let record = db.find((r) => r.id === key)
    const fields = Object.keys(record.entry)
    .sort((a, b) => a.localeCompare(b))
    .map(field => {
        return `${field}(${record.entry[field]})`
    })
return fields.join(", ")
}
return ""
}
const scanEntryByPrefix = (query, db) => {
    [command, timestamp, key, prefix] = query
    let record = db.find((r) => r.id === key)
    if(record) {
            const fields = Object.keys(record.entry)
            .filter((f) => f.startsWith(prefix))
                .filter(f => {
                    return timestamp >= f.timestamp && timestamp < f.ttl
                })
            .sort((a, b) => a.localeCompare(b))
            .map(field => {
                return `${field}(${record.entry[field]})`
            })
        return fields.join(", ") // this was an annoying requirement
    } else {
        return ""
    }
}

const getEntry = (query, db) => {
    const [command, timestamp, key, field] = query
    let record = db.find((r) => r.id === key)
    if(record && record.entry[field]) {
        if(!record.entry[field].tll){
            return record.entry[field]
        }
        if(timestamp >= record.timestamp && timestamp < record.entry[field].ttl) {
            return record.entry[field]
        }
    }
    return ""
}

const setTTL = (query, db) => {
    [command, timestamp, key, field, value, ttl] = query
    let record = db.find((r) => r.id === key)
    const ttl = Number(timestamp) + Number(ttl)
    if(!record){
        record = { timestamp: timestamp, id: key, entry: {}}
        record.entry[field] = {
            value: value,
            timestamp: timestamp,
            ttl: ttl
        }
        db.push(record)
        return ""
    }
    record.entry[field] = {
        value: value,
        timestamp: timestamp,
        ttl: ttl
    }
    return ""
}
const compareSetTTL = (query, db) => {
    [command, timestamp, key, field, expectedValue, newValue, ttl] = query
    const [command, timestamp, key, field, expectedValue, newValue] = query
// Check DB to see if the key exists.
    let record = db.find((r) => r.id === key)
    if(!record){
        return "false"
    }
    if(record.entry[field] && record.entry[field].value === expectedValue){
        record.entry[field] = {
            value: newValue,
            timestamp: timestamp,
            ttl: Number(timestamp) + Number(ttl)
        }
        return "true"
    }
    return "false"
}


    const actions = {
        "SET" : setEntry,
        "COMPARE_AND_SET" : compareAndSetEntry,
        "COMPARE_AND_DELETE" : compareAndDelete,
        "GET" : getEntry,
        "SCAN" : scanEntry,
        "SCAN_BY_PREFIX" : scanEntryByPrefix,
        "SET_WITH_TTL" : setTTL,
        "COMPARE_AND_SET_WITH_TTL": compareSetTTL,
    }

    const result = queries.map(query => {
        const command = query[0]
    // TODO check if the command exists
        return actions[command](query, memoryDB)
    })
    return result
}