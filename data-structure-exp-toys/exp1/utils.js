"use strict";

function randomNumFunc(a = 0, b) {
    if (b === undefined) {
        b = a;
        a = 0;
    }
    if (a > b) {
        let t = a;
        a = b;
        b = t;
    }
    return Math.floor(a + (b - a) * Math.random());
}


function debugOutput(obj) {
    console.log(JSON.parse(JSON.stringify(obj)));
}

function isListAllIntNumber(l) {
    for (let i = 0; i < l.length; i++) {
        if (!Number.isSafeInteger(l[i]))
            return false;
    }
    return true;
}

function isPossibility(n) {
    return Number.isFinite(n) && n >= 0 && n <= 1;
}

function isValueInList(n, l) {
    for (let i = 0; i < l.length; i++) {
        if (n === l[i])
            return true;
    }
    return false;
}

function resToString(res, peopleList) {
    if (res.message) {
        return res.message;
    }
    let s = `At time ${res.time}, Player ${peopleList[res.starter].name} started the event ${res.type[0]}, which belongs to the ${res.type[1]} events. `;
    switch (res.type[1]) {
        case "attack":
            s += `Player ${peopleList[res.receiver].name} is the target. `;
            if (res.success) {
                s += `They were attacked by ${res.damage} HP, ${res.type[2]}ly.`;
            }
            else
                s += "But failed!";
            break;
        case "heal":
            if (res.success) {
                s += `They healed themselves ${res.toValue} ${res.type[2].toUpperCase()}`;
                s += `, at the cost of ${res.fromValue} ` + (res.type[2] === "hp" ? "MP" : "HP") + ".";
            }
            else {
                s += "They tried healing themselves, but failed!";
            }
            break;
        case "magic":
            if (res.success) {
                s += `They used ${res.fromValue} MP to get more ${res.toValue} ${res.type[2].toUpperCase()}.`;
            }
            else {
                s += "They tried using some magic, but failed!";
            }
            break;
        case "return":
            s += `Their ${res.type[2].toUpperCase()} was returned to the normal value.`;
    }
    return s;
}

class Node {
    constructor(value, next) {
        this.value = value;
        this.next = next;
    }
}

class LinkedList {
    constructor() {
        this.head = new Node(null, null);
    }

    add(value) {
        const node = new Node(value, null);
        let t = this.head;
        while (t.next != null) {
            if (t.next.value.valueOf() > value.valueOf()) {
                break;
            }
            t = t.next;
        }
        // insert after t
        node.next = t.next;
        t.next = node;
    }

    pop() {
        if (!this.isEmpty()) {
            let ret = this.head.next.value;
            this.head.next = this.head.next.next;
            return ret;
        }
        else
            throw [this, "This linked list is empty!"];
    }

    getHead() {
        return this.head.next.value;
    }

    isEmpty() {
        return !this.head.next;
    }
}


module.exports = {
    LinkedList: LinkedList,
    randomNumFunc: randomNumFunc,
    debugOutput: debugOutput,
    isListAllIntNumber: isListAllIntNumber,
    isPossibility: isPossibility,
    isValueInList: isValueInList,
    resToString: resToString
};
