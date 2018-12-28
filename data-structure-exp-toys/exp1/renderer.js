"use strict";
window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.slim.min.js');
const bgApp = require('./simulation');
const fs = require('fs');
const utils = require('./utils');
const {dialog, getCurrentWindow} = require('electron').remote;

function startSimulation(config) {
    utils.debugOutput("start simulation");

    let sim = new bgApp.Simulation(
        config.peopleList, config.endTime
    );
    utils.debugOutput(sim.peopleList);

    return sim;
}


function parseSimulationConfig(strJson) {
    function parseErrorMsg(people, event, type) {
        return "People " + people + " , event " + event + " , type " + type + " error.";
    }

    try {
        let simulationConfigObj = JSON.parse(strJson);
        let peopleList = simulationConfigObj.peopleList;
        let endTime = simulationConfigObj.endTime;
        if (!Number.isSafeInteger(endTime) || endTime <= 0) {
            throw "Argument endTime error";
        }
        if (peopleList.length < 2) {
            throw "Too few people!";
        }
        for (let i = 0; i < peopleList.length; i++) {
            let name = peopleList[i].name;
            let hp = peopleList[i].hp;
            let pd = peopleList[i].pd;
            let mp = peopleList[i].mp;
            let md = peopleList[i].md;
            let events = peopleList[i].events;
            let eventSeq = peopleList[i].eventSeq;
            let freezeTime = peopleList[i].freezeTime;
            let priority = peopleList[i].priority;

            if (typeof name !== "string" || !utils.isListAllIntNumber([hp, pd, mp, md, freezeTime, priority])
                || hp < 0 || pd <= 0 ||
                mp <= 0 || md <= 0) {
                throw "People" + i + ": Argument name, hp, pd, mp, md, freezeTime or priority error. Check their type and value."
            }
            if (eventSeq.length === 0) {
                throw "eventSeq cannot be empty."
            }
            if (events.length === 0) {
                throw "events cannot be empty."
            }
            for (let j = 0; j < eventSeq.length; j++) {
                if (!Number.isSafeInteger(eventSeq[j]) || eventSeq[j] < 0 ||
                    eventSeq[j] >= events.length) {
                    throw "Argument eventSeq[" + j + "]error. Check type and value."
                }
            }
            for (let j = 0; j < events.length; j++) {
                let ename = events[j].name;
                let attributes = events[j].attributes;

                if (typeof ename !== "string") {
                    throw parseErrorMsg(i, j, "name")
                }
                switch (attributes[0]) {
                    case "attack":
                        if (!utils.isValueInList(attributes[1], ["physical", "magical"]) ||
                            !utils.isValueInList(attributes[2], ["leastHp", "leastMd", "leastPd", "leastMp"]) ||
                            !utils.isListAllIntNumber(attributes[3], attributes[4]) ||
                            attributes[3] > attributes[4] ||
                            !utils.isPossibility(attributes[5]) ||
                            attributes.length !== 6)
                            throw parseErrorMsg(i, j, "attack");
                        break;
                    case "heal":
                        if (!utils.isValueInList(attributes[1], ["hp", "mp"]) ||
                            !utils.isListAllIntNumber(attributes[2], attributes[3]) ||
                            attributes[2] < 0 || attributes[3] < 0 ||
                            !utils.isPossibility(attributes[4]) || attributes.length !== 5)
                            throw parseErrorMsg(i, j, "heal");
                        break;
                    case "magic":
                        if (!utils.isValueInList(attributes[1], ["pa", "pd", "ma", "md"]) ||
                            !utils.isListAllIntNumber(attributes[2], attributes[3], attributes[4]) ||
                            !utils.isPossibility(attributes[5]) || attributes[2] < 0 ||
                            attributes[3] < 0 || attributes[4] <= 0 || attributes.length !== 6)
                            throw parseErrorMsg(i, j, "magic");
                        break;
                    default:
                        throw parseErrorMsg(i, j, "unknown");
                }
            }
        }
        return simulationConfigObj;
    } catch (e) {
        utils.debugOutput(e);
        throw e;
    }
}

let thisSim = null;

$('#txtFileName').val("example.json");

$('#btnOpenFile').on('click', function (e) {
    dialog.showOpenDialog(getCurrentWindow(), {
        title: "Select JSON simulation file...",
        properties: ['openFile'],
        defaultPath: "./",
        filters: [
            {
                "name": "JSON files",
                extensions: ["json"]
            }
        ]
    }, function (files) {
        if (files !== undefined) {
            let file = files[0];
            $('#txtFileName').val(file);
        }
    });
});

let $persons;

$('#btnStart').on('click', function () {
    let fileName = $('#txtFileName').val();
    if (fileName.length === 0) {
        alert("Please select a file to load from!");
        return;
    }

    let content, fstat, simConfig;
    try {
        fstat = fs.lstatSync(fileName);
        if (!fstat.isFile()) {
            throw "ERROR: Not a regular file, refusing to open";
        }
        if (fstat.size >= 1000000) {
            throw "ERROR: File is too big, refusing to open";
        }
        content = fs.readFileSync(fileName, "utf-8");
        simConfig = parseSimulationConfig(content);
    } catch (e) {
        alert(e);
        return;
    }
    thisSim = startSimulation(simConfig);
    $('#new-simulation').hide();
    $('#simulation').show();
    $persons = [];
    for (let i = 0; i < thisSim.peopleList.length; i++) {
        let person = $('#personRow').clone();
        $persons.push(person);
        $('input', person).addClass('person-data');
        $('#personContainer').append(person);
        person.show();
    }
    updatePersons();
});

function updateBox($box, newVal) {
    let oldVal = $box.val();
    if (oldVal !== String(newVal)) {
        if (oldVal !== undefined && oldVal.length > 0) {
            if (Number(oldVal) < newVal) {
                $box.addClass('increased');
                setTimeout(function () {
                    $box.removeClass('updated');
                    $box.removeClass('increased');
                }, 100);
            }
            else if (Number(oldVal) > newVal) {
                $box.addClass('decreased');
                setTimeout(function () {
                    $box.removeClass('updated');
                    $box.removeClass('decreased');
                }, 100);
            }
            else {
                setTimeout(function () {
                    $box.removeClass('updated');
                    $box.removeClass('decreased');
                }, 100);
            }
            $box.addClass('updated');
        }
        $box.val(newVal);
    }
}

function updatePersons() {
    for (let i = 0; i < thisSim.peopleList.length; i++) {
        let person = $persons[i];
        let personInfo = thisSim.peopleList[i];
        let box;
        updateBox($('input[name="personName"]', person), personInfo.name);
        updateBox($('input[name="personHp"]', person), personInfo.hp);
        updateBox($('input[name="personMp"]', person), personInfo.mp);
        updateBox($('input[name="personPd"]', person), personInfo.pd + personInfo.pdOffset);
        updateBox($('input[name="personMd"]', person), personInfo.md + personInfo.mdOffset);
        if (personInfo.hp <= 0) {
            person.addClass("person-dead");
        }
    }
}

$('#nextEvent').on('click', function () {
    let ne = thisSim.nextEvent();
    let $console = $('#console');
    for (let i = ne.length - 1; i >= 0; i--) {
        $console.text(utils.resToString(ne[i], thisSim.peopleList) + "\n" + $console.text());
    }
    updatePersons();
    if (ne[0].message !== undefined) {
        $('#nextEvent').attr("disabled", "disabled");
        $('div.person:not(.person-dead)').addClass('person-winner');
    }
});
