new Vue({
    el: "#app",
    data() {
        //获取对象
        var video = document.getElementById('video');
        //var canvas = document.getElementById('canvas');
        //var context = canvas.getContext('2d');

        //显示实时时间
        //showTime();
        return {
            tableData: [{
                name: '王小虎',
                time: 320
            }, {
                name: '王小二',
                time: 100
            }, {
                name: '大美',
                time: 50
            }, {
                name: '小天',
                time: 1000
            }, {
                name: '小天',
                time: 500
            }, {
                name: '小天',
                time: 400
            }, {
                name: '小天',
                time: 230
            }]
        }
    },
    methods: {
        //关闭摄像头
        closeMedia() {
            if (!video.srcObject) return
            let stream = video.srcObject
            let tracks = stream.getTracks();
            tracks.forEach(track => {
                track.stop()
            })
        },

        //获得video摄像头区域
        getMedia() {
            let constraints = {
                video: {width: 1000, height: 1000},
                audio: true
            };
            //H5新媒体接口 navigator.mediaDevices.getUserMedia()
            let promise = navigator.mediaDevices.getUserMedia(constraints);
            promise.then(function (MediaStream) {
                video.srcObject = MediaStream;
                video.play();
            }).catch(function (PermissionDeniedError) {
                console.log(PermissionDeniedError);
            })
        },

        uploadImage() {
            setInterval(() => {
                //设置canvas大小
                canvas.width = 1000;
                canvas.height = 1000;
                //将video绘画在context上
                context.drawImage(video, 0, 0, 1000, 1000);
                var imgData = canvas.toDataURL();
                //imgData = imgData.replace(/^data:image\/(png|jpg);base64,/, "");
                console.log(imgData);
                //上传后端
                $.ajax({
                    url: "/xxxx.do",
                    type: "POST",
                    data: {"imgData": imgData},
                    success: function (data) {
                        console.log(data);
                        document.gauges.forEach(function (gauge) {
                            gauge.value = data.data
                        });
                    },
                    error: function () {
                        console.log("服务端异常！");
                    }
                });
            }, 0);
        },
        sortByTime(a, b) {
            return a.time - b.time;
        },
        showTime() {
            //设置时间
            document.getElementById('time').innerHTML = new Date().toLocaleString();
            setInterval("document.getElementById('time').innerHTML=new Date().toLocaleString();", 1000);
            //设置星期几
            var week = new Array('星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六');
            var mydd = new Date();
            var index = mydd.getDay();
            document.getElementById('day').innerHTML = week[index]
        },

        //开始
        start_video() {
            //开启摄像头
            this.getMedia();
            //获取每帧图片并上传给后台
            this.uploadImage();
            //开始计时
            startTime();
            $(function () {
                var ts = (new Date()).getTime() + 10000;
                $('#countdown').countdown({
                    timestamp: ts
                });
            });

            //处理按钮是否可用
            document.getElementById("start-button").disabled = true;
            document.getElementById("start-button").style.backgroundColor = 'grey';
            document.getElementById("stop-button").disable = false;
            document.getElementById("stop-button").style.backgroundColor = '';

        },

        //停止
        stop_video() {
            //关闭摄像头
            this.closeMedia();
            //关闭计时
            this.stopTime();
            //处理按钮是否可用
            document.getElementById("start-button").disabled = false;
            document.getElementById("start-button").style.backgroundColor = '';
            document.getElementById("stop-button").disable = true;
            document.getElementById("stop-button").style.backgroundColor = 'grey';
        },

        //弹窗设置计时模式
        set_mode() {
            //var choiceWindow = window.open('detecting.html')
            let options = {
                title: 'title',
                body: 'body'
            }
            let myNotification = new window.Notification(options.title, options)
            myNotification.onclick = () => {
                this._setState({
                    message: 'clicked'
                })
            }
        }
    },
    mounted:{}
})

