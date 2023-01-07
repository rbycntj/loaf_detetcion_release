new Vue({
    el: "#app",

    data() {
        //获取对象
        return {
            URL: "http://127.0.0.1:5000",
            imgSrc: "img/tile_bg.jpg",
            name:"user",
            activeName:"first",
            id: 1,
            record:[],
            user_rank:0,
            total_record_time:0,
            friendTable: [],
            AllSortTable: [],
        }
    },
    methods: {
        //个人信息
        getUserInfo() {
          axios({
                method: 'get',
                url: this.URL + '/info/' + this.id
            }).then(resp => {
                if (resp.data.flag == true) {
                    //设置头像
                    this.imgSrc = 'http://rnswweke3.hd-bkt.clouddn.com/' + resp.data.obj.img + '.jpg'
                    this.name = resp.data.obj.username
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        //好友排名
        getFriendSort(){
            let id = window.sessionStorage.getItem("id");
            console.log(id);
            axios({
                method: 'get',
                url: this.URL+'/ranks/friend/'+id,
            })
                .then(resp => {
                    console.log(resp);
                    if (resp.data.flag === true) {
                        this.friendTable = resp.data.obj;
                    } else {
                        this.$message({
                            type: "error",
                            message: resp.data.msg
                        })
                    }
                });
        },
        //总排名
        getAllSort() {
            let id = window.sessionStorage.getItem("id");
            axios({
                method: 'get',
                url: this.URL + '/ranks/30',
            })
                .then(resp => {
                    console.log(resp);
                    if (resp.data.flag === true) {
                        this.AllSortTable = resp.data.obj;
                    } else {
                        this.$message({
                            type: "error",
                            message: resp.data.msg
                        })
                    }
                });
        },
        //个人排名
        get_user_rank(){
            let id = window.sessionStorage.getItem("id");
            axios({
                method: 'get',
                url: this.URL+'/rank/' + id,
            })
                .then(resp => {
                    console.log(resp);
                    if (resp.data.flag === true) {
                        this.user_rank = resp.data.obj[0];
                        this.total_record_time = resp.data.obj[1];
                    } else {
                        if (resp.data.msg =="获取排名失败"){
                            this.$message({
                                message: "暂无个人排名",
                            })
                        }
                    }
                });
        },

        //弹窗设置计时模式
        set_mode() {
            const {ipcRenderer} = require('electron');
            ipcRenderer.send('main:choice');
            console.log('starts-button clicked');

            ipcRenderer.on("record", (event, data) => {
                console.log(data)
                let left_region = document.getElementsByClassName('left-region')[0];
                let right_region = document.getElementsByClassName('right-region')[0];
                if(right_region && left_region ){
                    console.log(right_region, left_region)
                }
                left_region.classList.toggle('expand');
                right_region.classList.toggle('hide');
                setTimeout(function(){
                    right_region.style.display = 'none';
                },500);
                // jump
                setTimeout(function (){
                    window.location.replace("recording.html");
                }, 600)
            })
        },
    },
    mounted() {
        this.id = window.sessionStorage.getItem("id");
        this.getUserInfo();
        this.getFriendSort();
        this.getAllSort();
        this.get_user_rank();
    }
})

