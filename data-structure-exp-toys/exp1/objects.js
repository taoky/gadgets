"use strict";

class Person {
    constructor(itemDictionary, id) {
        this.name = itemDictionary["name"];
        this.id = id;
        this.hp = itemDictionary["hp"];
        this.pd = itemDictionary["pd"];
        this.mp = itemDictionary["mp"];
        this.md = itemDictionary["md"];
        this.events = itemDictionary["events"];
        this.eventSeq = itemDictionary["eventSeq"];
        this.freezeTime = itemDictionary["freezeTime"];
        this.priority = itemDictionary["priority"];
        this.isAlive = true;
        this.paOffset = 0;
        this.maOffset = 0;
        this.pdOffset = 0;
        this.mdOffset = 0;

    }

    hurt(attack) {
        if (!this.isAlive) {
            throw "Cannot hurt the dead!";
        }
        this.hp -= attack;
        if (this.hp <= 0)
            return this.isAlive = false;
        else return true;
    }

    // convert(type, from, to) {
    //
    // }

    resetAtt(type) {
        switch (type) {
            case "pa":
                this.paOffset = 0;
                break;
            case "ma":
                this.maOffset = 0;
                break;
            case "pd":
                this.pdOffset = 0;
                break;
            case "md":
                this.mdOffset = 0;
                break;
            default:
                throw "Unknown Type to Reset!";
        }
    }

    eventGenerate(nowTime, order) {
        order = order % this.eventSeq.length;
        return new Event(this.events[this.eventSeq[order]], {
                "starterId": this.id,
                "eventOrder": order,
                "priority": this.priority
            },
            nowTime + this.freezeTime);
    }
}

class Event {
    constructor(action, eventAtt, occurTime, sortedByPriority = false) {
        this.action = action;
        this.eventAtt = eventAtt;
        this.occurTime = occurTime;
        this.sortedByPriority = sortedByPriority;
    }

    valueOf() {
        // to be sorted in the order of occurTime
        if (!this.sortedByPriority)
            return this.occurTime;
        else
            return this.eventAtt["priority"];
    }
}

module.exports = {
    Person: Person,
    Event: Event,
    // parseDictToPerson: parseDictToPerson
};