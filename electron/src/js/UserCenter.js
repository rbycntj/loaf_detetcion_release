baseUrl = "http://127.0.0.1:5000"
new Vue({
    el: "#app",


    data: {
        form: {
            username: '',
            gender: '',
            password: '',
            telephone: '',
        },
        tableData: [],
        messageData: [],
        userimg: 'http://rnswweke3.hd-bkt.clouddn.com/1.jpg',
        radio: '1',

        update_username: '',
        update_gender: '',
        update_password: '',
        update_telephone: '',


        dialogFormVisible: false,
        dialogImgVisible: false,
        dialogMessage: false,
        formLabelWidth: '70px',

        id: 1,
        loading: false,
        input_telephone: ''

    },
    methods: {
        // ifExit() {
        //     if (document.referrer == "") {
        //         window.location.href = "../html/index.html"
        //     } else {
        //         window.location.href = document.referrer;
        //     }
        // },

        cancelDialogImg() {
            this.dialogImgVisible = false;
            this.radio = '1'
        },
        confirmDialogImg() {
            this.dialogImgVisible = false;
            axios({
                method: 'post',
                url: baseUrl + '/info',
                data: {
                    "id": this.id,
                    "img": this.radio
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: resp.data.msg,
                    });
                    this.showBasicInfo();
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            }).finally(() => {
                this.radio = '1'
            })
        },

        confirmDialogForm() {
            if (this.update_username == null || this.update_password == null || this.update_telephone == null || this.update_telephone == '' || this.update_username == '' || this.update_password == '') {
                this.$message({
                    type: "warning",
                    message: '输入不能为空'
                })
                return;
            }
            if (this.update_gender == null || this.update_gender == '' || this.update_gender == "未指定") {
                this.$message({
                    type: "warning",
                    message: '未指定性别'
                })
                return;
            }
            this.dialogFormVisible = false
            axios({
                method: 'put',
                url: baseUrl + '/info',
                data: {
                    "id": this.id,
                    "username": this.update_username,
                    "password": this.update_password,
                    "gender": (this.update_gender == '男' ? 0 : 1)
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: resp.data.msg,
                    });
                    this.showBasicInfo();
                    this.reload();
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.masg,
                    });
                }
            }).finally(() => {
                this.update_username = "";
                this.update_password = "";
                this.update_telephone = "";
                this.update_gender = "";
            })
        },
        cancelDialogForm() {
            this.dialogFormVisible = false;
            this.update_username = "";
            this.update_password = "";
            this.update_telephone = "";
            this.update_gender = "";
        },

        updateBtn() {
            this.dialogFormVisible = true
            this.update_username = this.form.username
            this.update_password = this.form.password
            this.update_telephone = this.form.telephone
            this.update_gender = this.form.gender
        },
        //查询基础信息
        showBasicInfo() {
            axios({
                method: 'get',
                url: baseUrl + '/info/' + this.id
            }).then(resp => {
                if (resp.data.flag == true) {
                    //设置头像
                    this.userimg = 'http://rnswweke3.hd-bkt.clouddn.com/' + resp.data.obj.img + '.jpg'
                    this.form.username = resp.data.obj.username
                    this.form.gender = resp.data.obj.gender == 0 ? '男' : resp.data.obj.gender == 1 ? '女' : '未指定'
                    this.form.password = resp.data.obj.password
                    this.form.telephone = resp.data.obj.telephone
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        showSelfAndFriendRanks() {
            axios({
                method: 'get',
                url: baseUrl + '/ranks/friend/' + this.id
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.tableData = resp.data.obj;
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        query_add_friends_msg() {
            axios({
                method: 'get',
                url: baseUrl + '/friends/' + this.id
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.messageData = resp.data.obj;
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        handleAccept(fid) {
            axios({
                method: 'put',
                url: baseUrl + '/friend',
                data: {
                    "uid": this.id,
                    "fid": fid
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: resp.data.msg,
                    });
                    this.reload()
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        handleDelete(fid) {
            axios({
                method: 'post',
                url: baseUrl + '/friend',
                data: {
                    "uid": this.id,
                    "fid": fid
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: resp.data.msg,
                    });
                    this.reload()
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            })
        },
        cancelAddFriend() {
            this.input_telephone = "";
            this.dialogMessage = false
        },
        confirmAddFriend() {
            axios({
                method: 'post',
                url: baseUrl + '/friend/' + this.id,
                data: {
                    "telephone": this.input_telephone,
                }
            }).then(resp => {
                if (resp.data.flag == true) {
                    this.$message({
                        type: 'success',
                        message: resp.data.msg,
                    });
                } else {
                    this.$message({
                        type: 'error',
                        message: resp.data.msg,
                    });
                }
            }).finally(()=>{
                this.input_telephone = "";
                this.dialogMessage = false
            })
        },
        reload() {
            this.showSelfAndFriendRanks();
            this.query_add_friends_msg();
        },
        ifExit() {
            window.location.replace('index.html')
        }
    },
    mounted() {
        this.id = window.sessionStorage.getItem("id");
        console.log(this.id)
        this.showBasicInfo();
        this.showSelfAndFriendRanks();
        this.query_add_friends_msg();
    }
})



