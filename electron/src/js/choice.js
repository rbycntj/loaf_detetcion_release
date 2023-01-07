new Vue({
    el: "#app",
    data() {
        return{
            radio1: '正计时',
            value2: 25,
            value3: new Date(),
            clockwise: false,
            setTimeLen: 5,
        }
    },
    methods: {
        handleChange(value) {
            console.log(value);
        },
        start_record() {
            switch (this.radio1) {
                case "正计时":
                    this.clockwise = true
                    break
                case "倒计时":
                    this.clockwise = false
                    this.setTimeLen = this.value2 * 60
                    break
                case "指定截止":
                    this.clockwise = false
                    const currentTime = new Date();
                    console.log(currentTime);
                    console.log(this.value3)
                    this.setTimeLen = Math.floor(this.value3.getTime()-currentTime.getTime())/1000
                    if (this.setTimeLen <= 0) {
                        this.$message({
                            type: "error",
                            message: '结束时间不得早于当前时间'
                        })
                        return
                    }
            }
            // main窗口做切换动效
            const {ipcRenderer} = require('electron');
            ipcRenderer.send('send-data', [this.clockwise, this.setTimeLen]);
            // 关闭当前choice子窗口
            window.close()
        }
    },
    mounted: {

    }
})