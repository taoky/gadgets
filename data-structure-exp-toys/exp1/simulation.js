"use strict";

const objects = require('./objects');
const utils = require('./utils');

// const app = require('electron').app;

class Simulation {
    constructor(peopleDictList, endTime) {
        this.peopleDictList = peopleDictList;
        this.endTime = endTime;
        this.peopleList = [];

        for (let i = 0; i < this.peopleDictList.length; i++) {
            this.peopleList.push(new objects.Person(this.peopleDictList[i], i));
        }

        if (this.peopleList.length < 2)
            throw "Too few people for simulation. At least 2.";

        // simulation variables
        this.eventList = new utils.LinkedList();

        // initialize eventList
        for (let i = 0; i < this.peopleList.length; i++) {
            this.eventList.add(this.peopleList[i].eventGenerate(0, 0));
        }
    }

    nextEvent() {
        function adjustEventAndAdd(e, ll) {
            e.sortedByPriority = true;
            ll.add(e);
        }

        let eventThisCycle = new utils.LinkedList();
        let ret = [];
        let e = this.eventList.pop();

        adjustEventAndAdd(e, eventThisCycle);

        while (!this.eventList.isEmpty() && this.eventList.getHead().occurTime === e.occurTime) {
            let e = this.eventList.pop();
            adjustEventAndAdd(e, eventThisCycle);
        }

        function attack(self, event) {
            let att = event.action["attributes"];
            let eAtt = event.eventAtt;
            let time = event.occurTime;
            let pid = eAtt["starterId"];
            let order = eAtt["eventOrder"];

            let attackType = att[1];
            let attackTarget = null;

            function retPidLeastEle(str, pid, pList) {
                let ret = -1;
                for (let i = 0; i < pList.length; i++) {
                    if (i !== pid && pList[i].isAlive && (ret === -1 ? true : pList[i][str] < pList[ret][str])) {
                        ret = i;
                    }
                }
                return ret;
            }

            switch (att[2]) {
                case "leastHp":
                    attackTarget = retPidLeastEle("hp", pid, self.peopleList);
                    break;
                case "leastPd":
                    attackTarget = retPidLeastEle("pd", pid, self.peopleList);
                    break;
                case "leastMd":
                    attackTarget = retPidLeastEle("md", pid, self.peopleList);
                    break;
                case "leastMp":
                    attackTarget = retPidLeastEle("mp", pid, self.peopleList);
                    break;
                default:
                    throw "Undefined Attack Type!";
            }

            let possibility = att[5];
            let success = true;
            let damage = null;
            if (Math.random() > possibility || attackTarget === -1) {
                success = false;
            }
            else {
                let attackLeast = att[3];
                let attackMost = att[4];
                let attack = utils.randomNumFunc(attackLeast, attackMost);

                // start attacking
                if (attackType === "physical") {
                    damage = Math.max(Math.min(attack + self.peopleList[pid].paOffset - Math.min(Math.round((self.peopleList[attackTarget].pd +
                        self.peopleList[attackTarget].pdOffset) * 0.1), Number.MAX_SAFE_INTEGER), Number.MAX_SAFE_INTEGER), 1); // at least hurt 1 hp
                }
                else
                    damage = Math.max(Math.min(attack + self.peopleList[pid].maOffset - Math.min(Math.round((self.peopleList[attackTarget].md +
                        self.peopleList[attackTarget].mdOffset) * 0.1), Number.MAX_SAFE_INTEGER), Number.MAX_SAFE_INTEGER), 1);

                self.peopleList[attackTarget].hurt(damage);

            }
            // add next event
            self.eventList.add(self.peopleList[pid].eventGenerate(time, order + 1));
            // return information
            return {
                "time": time,
                "type": [event.action["name"], "attack", attackType],
                "starter": pid,
                "receiver": attackTarget,
                "success": success,
                "damage": damage
            }
        }

        function heal(self, event) {
            let att = event.action["attributes"];
            let eAtt = event.eventAtt;
            let time = event.occurTime;
            let pid = eAtt["starterId"];
            let order = eAtt["eventOrder"];

            let healType = att[1];
            let possibility = att[4];
            let success = true;
            if (Math.random() > possibility) {
                success = false;
            }
            else {
                switch (healType) {
                    case "hp":
                        let fromMp = att[2];
                        let toHp = att[3];
                        if (self.peopleList[pid].mp < fromMp) {
                            success = false;
                            break;
                        }
                        self.peopleList[pid].hp += toHp;
                        self.peopleList[pid].hp = Math.min(self.peopleList[pid].hp, Number.MAX_SAFE_INTEGER);
                        self.peopleList[pid].mp -= fromMp;
                        break;
                    case "mp":
                        let fromHp = att[2];
                        let toMp = att[3];
                        if (self.peopleList[pid].hp <= fromHp) {
                            success = false;
                            break;
                        }
                        self.peopleList[pid].mp += toMp;
                        self.peopleList[pid].mp = Math.min(self.peopleList[pid].mp, Number.MAX_SAFE_INTEGER);
                        self.peopleList[pid].hp -= fromHp;
                        break;
                    default:
                        throw "Unknown Heal Type!";
                }
            }
            self.eventList.add(self.peopleList[pid].eventGenerate(time, order + 1));

            return {
                "time": time,
                "type": [event.action["name"], "heal", healType],
                "starter": pid,
                "fromValue": att[2],
                "toValue": att[3],
                "success": success
            };
        }

        function magic(self, event) {
            // this function is for a temporary magic to work.
            let att = event.action["attributes"];
            let eAtt = event.eventAtt;
            let time = event.occurTime;
            let pid = eAtt["starterId"];
            let order = eAtt["eventOrder"];

            let magicType = att[1];
            let fromMp = att[2];
            let toValue = att[3];
            let keepTime = att[4];
            let possibility = att[5];
            let success = true;
            if (Math.random() > possibility || self.peopleList[pid].mp < fromMp) {
                success = false;
            }
            else {
                switch (magicType) {
                    case "pa":
                        self.peopleList[pid].paOffset += toValue;
                        self.peopleList[pid].paOffset = Math.min(self.peopleList[pid].paOffset, Number.MAX_SAFE_INTEGER);
                        break;
                    case "ma":
                        self.peopleList[pid].maOffset += toValue;
                        self.peopleList[pid].maOffset = Math.min(self.peopleList[pid].maOffset, Number.MAX_SAFE_INTEGER);
                        break;
                    case "pd":
                        self.peopleList[pid].pdOffset += toValue;
                        self.peopleList[pid].pdOffset = Math.min(self.peopleList[pid].pdOffset, Number.MAX_SAFE_INTEGER);
                        break;
                    case "md":
                        self.peopleList[pid].mdOffset += toValue;
                        self.peopleList[pid].mdOffset = Math.min(self.peopleList[pid].mdOffset, Number.MAX_SAFE_INTEGER);
                        break;
                }
                self.eventList.add(new objects.Event({
                    "name": "Return to normal after: " + event.action["name"],
                    "attributes": ["return", magicType]
                }, {
                    "starterId": pid,
                    "eventOrder": -1,
                    "priority": self.peopleList[pid].priority
                }, Math.min(time + keepTime, Number.MAX_SAFE_INTEGER)));
            }
            self.eventList.add(self.peopleList[pid].eventGenerate(time, order + 1));

            return {
                "time": time,
                "type": [event.action["name"], "magic", magicType],
                "starter": pid,
                "fromValue": fromMp,
                "toValue": toValue,
                "success": success
            };
        }

        function retFunc(self, event) {
            let att = event.action["attributes"];
            let eAtt = event.eventAtt;
            let time = event.occurTime;
            let pid = eAtt["starterId"];

            let resetType = att[1];
            self.peopleList[pid].resetAtt(resetType);

            return {
                "time": time,
                "type": [event.action["name"], "reset", resetType],
                "starter": pid,
                "success": true
            };
        }

        while (!eventThisCycle.isEmpty()) {
            let thisEvent = eventThisCycle.pop();
            let pid = thisEvent.eventAtt["starterId"];

            // is there only one survived?
            let deadCnt = 0;
            for (let i = 0; i < this.peopleList.length; i++) {
                if (!this.peopleList[i].isAlive) deadCnt++;
            }
            if (deadCnt === this.peopleList.length - 1) {
                ret.push({
                    "message": "All others are dead. Simulation has ended."
                });
                break;
            }

            if (thisEvent.occurTime > this.endTime) {
                ret.push({
                    "message": "Time > endTime. Simulation has ended."
                });
                break;
            }
            console.log(thisEvent);
            if (!this.peopleList[pid].isAlive) continue;
            switch (thisEvent.action["attributes"][0]) {
                case "attack":
                    ret.push(attack(this, thisEvent));
                    break;
                case "heal":
                    ret.push(heal(this, thisEvent));
                    break;
                case "magic":
                    ret.push(magic(this, thisEvent));
                    break;
                case "return":
                    ret.push(retFunc(this, thisEvent));
                    break;
                default:
                    throw "Unknown Event Type!";
            }
        }

        return ret;
    }
}

module.exports = {
    Simulation: Simulation
};