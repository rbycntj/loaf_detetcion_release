const request = require('electron-request');
const axios = require("axios");
const {ipcRenderer} = require('electron');

const video = document.getElementById('video');
video.style.display = "none";
const canvas = document.getElementById('helper-canvas');
canvas.style.display = "none";
const textConnected = document.getElementById('status-text-connected');
textConnected.style.display = 'none';
const textDisconnected = document.getElementById('status-text-disconnected');
textDisconnected.style.display = 'inline';
const textTimer = document.getElementById('timer-text');
const contentRecording = document.getElementById('content-recording');
contentRecording.style.display = 'block';
const contentResults = document.getElementById('content-results');
contentResults.style.display = 'none';

var CW_NORM = 0;    // 0: 正计时正常退出
var NW_NORM = 1;    // 1：倒计时到点退出
var NW_AHEAD = 2;   // 2：倒计时提前退出
var ERR_CAM = 3;    // 3：摄像头无法开启
const fullScore = 100;

let startTime = 0;
let endTime = 0;
let mediaStream = null;
let terminated = false;
let record_id = -1;
let user_id = window.sessionStorage.getItem("id");
let baseUrl = "http://114.116.217.11:8080";
let mode = {
    clockwise: true,
    setTimeLen: 5,
    exitMode: CW_NORM,
}
let finalResult = {
    head: [],
    face: [],
    invalid: [],
    eyeClosed: [],
    mouth: [],
    timeStart: 0,
    timeEnd: 0,
    empty: true,
    score: 0,
};
let message = [
    "本次专注得分"+"<score>"+"分，请再接再厉",
    "本次专注得分"+"<score>"+"分，为坚持点赞",
    "很遗憾，没有坚持到最后,得分"+"<score>"+"分",
    "无法启用摄像头",
]
let resultQueue = [];
let currentStatus = {
    head: 0,
    face: 0,
    invalid: false,
    eyeClosed: false,
    mouth: 0,
};
let scoreCalc = {
    invalidWeight: 0.5,
    headWeight: 0.2,
    eyeWeight: 0.1,
    mouthWeight: 0.1,
    faceWeight: 0.1,

    invalidPercent: 0,
    headPercent: 0,
    eyePercent: 0,
    mouthPercent: 0,
    facePercent: 0,
};

ipcRenderer.on("get_data", (event, data) => {
    console.log(data)
    mode.clockwise = data[0]
    mode.setTimeLen = data[1]
})

document.getElementById('quit-button').addEventListener('click', () => {
    if (mode.clockwise) {
        mode.exitMode = CW_NORM
    }else{
        mode.exitMode = NW_AHEAD
    }
    quit()
});

function quit() {
    terminated = true;
    if (mediaStream !== null) {
        mediaStream.getTracks().forEach(function(track) {
            track.stop();
        });
    }
    contentRecording.style.display = 'none';
    contentResults.style.display = 'block';

    finalResult.timeEnd = Date.now();
    if (finalResult.empty || mode.exitMode == ERR_CAM) {
        document.getElementById('results-chart').style.display = 'none';
        if (mode.exitMode == ERR_CAM) {
            document.getElementById('nothing-text').innerHTML= message[ERR_CAM]
        }
        // 无效学习记录
        if(record_id !== -1){
            axios({
                method: 'put',
                url: baseUrl + '/record/' + user_id,
                data: {
                    "record_id": record_id,
                    "valid": 0,
                    "score": 0
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: '学习记录上传成功',
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        }
        return;
    }
    else {
        document.getElementById('nothing-text').style.display = 'none';
    }
    const timeAll = finalResult.timeEnd - finalResult.timeStart;

    const chart1 = document.getElementById('chart-1');
    while (chart1.firstChild) { chart1.removeChild(chart1.lastChild); }
    const chart2 = document.getElementById('chart-2');
    while (chart2.firstChild) { chart2.removeChild(chart2.lastChild); }
    const chart3 = document.getElementById('chart-3');
    while (chart3.firstChild) { chart3.removeChild(chart3.lastChild); }
    const chart4 = document.getElementById('chart-4');
    while (chart4.firstChild) { chart4.removeChild(chart4.lastChild); }
    const chart5 = document.getElementById('chart-5');
    while (chart5.firstChild) { chart5.removeChild(chart5.lastChild); }

    let percent;
    for (let i = 0, curr = false, prevTime = finalResult.timeStart; i < finalResult.invalid.length + 1; ++i) {
        const element = document.createElement("div");
        element.className = `progress-bar ${curr ? 'bg-danger' : 'bg-light'}`;
        if (i === finalResult.invalid.length){
            percent = (finalResult.timeEnd - prevTime) / timeAll;
            element.style.width = `${percent * 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.invalidPercent += percent;
            }
        }else {
            percent = (finalResult.invalid[i][1] - prevTime) / timeAll
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.invalidPercent += percent;
            }
        }
        chart1.appendChild(element);
        if (i !== finalResult.invalid.length) {
            curr = finalResult.invalid[i][0];
            prevTime = finalResult.invalid[i][1];
        }
    }
    for (let i = 0, curr = 0, prevTime = finalResult.timeStart; i < finalResult.head.length + 1; ++i) {
        const element = document.createElement("div");
        element.className = `progress-bar ${curr === 1 ? 'bg-warning' : (curr === 2 ? 'bg-danger' : 'bg-light')}`;
        if (i === finalResult.head.length){
            percent = (finalResult.timeEnd - prevTime) / timeAll;
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.headPercent += percent;
            }
        }else {
            percent = (finalResult.head[i][1] - prevTime) / timeAll;
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.headPercent += percent;
            }
        }
        chart2.appendChild(element);
        if (i !== finalResult.head.length) {
            curr = finalResult.head[i][0];
            prevTime = finalResult.head[i][1];
        }
    }
    for (let i = 0, curr = 0, prevTime = finalResult.timeStart; i < finalResult.face.length + 1; ++i) {
        const element = document.createElement("div");
        element.className = `progress-bar ${curr === 1 ? 'bg-warning' : (curr === 2 ? 'bg-danger' : 'bg-light')}`;
        if (i === finalResult.face.length){
            percent = (finalResult.timeEnd - prevTime) / timeAll;
            element.style.width = `${ percent * 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.facePercent += percent;
            }
        }else {
            percent = (finalResult.face[i][1] - prevTime) / timeAll;
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.facePercent += percent;
            }
        }
        chart5.appendChild(element);
        if (i !== finalResult.face.length) {
            curr = finalResult.face[i][0];
            prevTime = finalResult.face[i][1];
        }
    }
    for (let i = 0, curr = 0, prevTime = finalResult.timeStart; i < finalResult.mouth.length + 1; ++i) {
        const element = document.createElement("div");
        element.className = `progress-bar ${curr === 1 ? 'bg-warning' : (curr === 2 ? 'bg-danger' : 'bg-light')}`;
        if (i === finalResult.mouth.length){
            percent = (finalResult.timeEnd - prevTime) / timeAll
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.mouthPercent += percent;
            }
        }else {
            percent = (finalResult.mouth[i][1] - prevTime) / timeAll
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.mouthPercent += percent;
            }
        }
        chart4.appendChild(element);
        if (i !== finalResult.mouth.length) {
            curr = finalResult.mouth[i][0];
            prevTime = finalResult.mouth[i][1];
        }
    }
    for (let i = 0, curr = false, prevTime = finalResult.timeStart; i < finalResult.eyeClosed.length + 1; ++i) {
        const element = document.createElement("div");
        element.className = `progress-bar ${curr ? 'bg-danger' : 'bg-light'}`;
        if (i === finalResult.eyeClosed.length){
            percent = (finalResult.timeEnd - prevTime) / timeAll
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.eyePercent += percent;
            }
        }else {
            percent = (finalResult.eyeClosed[i][1] - prevTime) / timeAll
            element.style.width = `${ percent* 100}%`;
            if(element.className !== "progress-bar bg-light"){
                scoreCalc.eyePercent += percent;
            }
        }
        chart3.appendChild(element);
        if (i !== finalResult.eyeClosed.length) {
            curr = finalResult.eyeClosed[i][0];
            prevTime = finalResult.eyeClosed[i][1];
        }
    }
    // TODO: upload results here
    // calc score
    let invalidScore = fullScore * (1-scoreCalc.invalidPercent) * scoreCalc.invalidWeight;
    let headScore = fullScore * (1-scoreCalc.headPercent) * scoreCalc.headWeight;
    let eyeScore = fullScore * (1-scoreCalc.eyePercent) * scoreCalc.eyeWeight;
    let mouthScore = fullScore * (1-scoreCalc.mouthPercent) * scoreCalc.mouthWeight;
    let faceScore = fullScore * (1-scoreCalc.facePercent) * scoreCalc.faceWeight;
    document.getElementById("invalidScore").innerHTML = parseInt(invalidScore) ;
    document.getElementById("headScore").innerHTML = parseInt(headScore);
    document.getElementById("eyeScore").innerHTML = parseInt(eyeScore);
    document.getElementById("mouthScore").innerHTML = parseInt(mouthScore);
    document.getElementById("faceScore").innerHTML = parseInt(faceScore);
    finalResult.score += parseInt(invalidScore) + parseInt(headScore) + parseInt(eyeScore) + parseInt(mouthScore) + parseInt(faceScore);
    if (mode.exitMode === NW_AHEAD){
        finalResult.score = 0
    }
    console.log(finalResult.score)

    message[mode.exitMode] = message[mode.exitMode].replace("<score>",finalResult.score.toString());
    document.getElementById("message").innerHTML = message[mode.exitMode];

    if(record_id !== -1){
        axios({
            method: 'put',
            url: baseUrl + '/record/' + user_id,
            data: {
                "record_id": record_id,
                "valid": 1,
                "score": finalResult.score
            }
        }).then(resp => {
            if (resp.data.flag == true) {
                this.$message({
                    type: 'success',
                    message: '学习记录上传成功',
                });
            } else {
                this.$message({
                    type: 'error',
                    message: resp.data.msg,
                });
            }
        })
    }
}

document.getElementById('homepage-button').addEventListener('click', () => {
    window.location.replace('index.html')
});

navigator.getUserMedia({video: true, audio: false}, (localMediaStream) => {
    mediaStream = localMediaStream;
    video.srcObject = localMediaStream;
    video.autoplay = true;
    video.addEventListener('play', () => {
        // 添加新的学习记录
        axios({
            method: 'post',
            url: baseUrl + '/record/' + user_id,
        }).then(resp => {
            if (resp.data.flag == true) {
                console.log("添加新的学习记录success")
                record_id = resp.data.obj
            } else {
                this.$message({
                    type: 'error',
                    message: resp.data.msg,
                });
            }
        })
        const timeoutCallback = async () => {
            if (terminated)
                return;
            const currentTime = Date.now();
            let timeElapsed = Math.floor((currentTime - startTime) / 1000);
            if (!mode.clockwise) {
                endTime = startTime + mode.setTimeLen * 1000;
                timeElapsed = Math.floor((endTime - currentTime) / 1000);
            }
            const elapsedSeconds = timeElapsed % 60;
            const elapsedMinutes = (timeElapsed - elapsedSeconds) / 60 % 60;
            const elapsedHours = (timeElapsed - elapsedSeconds - elapsedMinutes * 60) / 60;

            textTimer.innerText = `${String(elapsedHours).padStart(2, '0')}:${String(elapsedMinutes).padStart(2, '0')}:${String(elapsedSeconds).padStart(2, '0')}`

            if(!mode.clockwise && currentTime > endTime){
                mode.exitMode = NW_NORM;
                quit()
            }

            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/jpeg", .1);

            const url = `http://114.116.217.11:5000/process?frame=${0}`;
            const defaultOptions = {
                method: 'POST',
                body: imageData,
                followRedirect: true,
                maxRedirectCount: 20,
                timeout: 500,
                size: 0,
            };
            try {
                const response = await request(url, defaultOptions);
                const data = await response.json();
                if (resultQueue.length === 10) {
                    let headDownCount = 0;
                    let headElsewhereCount = 0;
                    let eyeClosedCount = 0;
                    let mouthSpeakingCount = 0;
                    let mouthYawnCount = 0;
                    let faceNearCount = 0;
                    let faceFarCount = 0;
                    let invalidCount = 0;
                    for (let i = 0; i < 10; ++i) {
                        const data = resultQueue[i];
                        if (!data.valid) invalidCount += 1;
                        else {
                            if (data.down) headDownCount += 1;
                            if (!data.down && !data.forward) headElsewhereCount += 1;
                            if (data.eye === 1) eyeClosedCount += 1;
                            if (data.face_depth === 1) faceNearCount += 1;
                            if (data.face_depth === 2) faceFarCount += 1;
                            if (data.mouth_status === 1) mouthSpeakingCount += 1;
                            if (data.mouth_status === 2) mouthYawnCount += 1;
                        }
                    }
                    if (finalResult.empty) {
                        finalResult.timeStart = currentTime;
                        finalResult.empty = false;
                    }
                    const head = headDownCount > 5 ? 2 : (headElsewhereCount > 5 ? 1 : 0);
                    const face = faceNearCount > 5 ? 1 : (faceFarCount > 5 ? 2 : 0);
                    const mouth = mouthYawnCount > 5 ? 2 : (mouthSpeakingCount > 5 ? 1 : 0);
                    const invalid = invalidCount > 5;
                    const eyeClosed = eyeClosedCount > 5;
                    if (head !== currentStatus.head) {
                        currentStatus.head = head;
                        finalResult.head.push([head, currentTime]);
                    }
                    if (face !== currentStatus.face) {
                        currentStatus.face = face;
                        finalResult.face.push([face, currentTime]);
                    }
                    if (mouth !== currentStatus.mouth) {
                        currentStatus.mouth = mouth;
                        finalResult.mouth.push([mouth, currentTime]);
                    }
                    if (invalid !== currentStatus.invalid) {
                        currentStatus.invalid = invalid;
                        finalResult.invalid.push([invalid, currentTime]);
                    }
                    if (eyeClosed !== currentStatus.eyeClosed) {
                        currentStatus.eyeClosed = eyeClosed;
                        finalResult.eyeClosed.push([eyeClosed, currentTime]);
                    }
                }
                if (resultQueue.length < 10) {
                    resultQueue.push(data);
                } else {
                    resultQueue.shift();
                    resultQueue.push(data);
                }
                textConnected.style.display = 'inline';
                textDisconnected.style.display = 'none';
            } catch (e) {
                textConnected.style.display = 'none';
                textDisconnected.style.display = 'inline';
            }
            if (!terminated)
                setTimeout(timeoutCallback, 200);
        };
        startTime = Date.now();
        endTime = startTime + mode.setTimeLen * 1000;
        if (!terminated)
            setTimeout(timeoutCallback, 200);
    });
    console.log("what")
}, () => {
    alert('无法启用摄像头');
    // TODO: exit this page after telling user that webcam could not be opened
    mode.exitMode = ERR_CAM;
    quit()
});


