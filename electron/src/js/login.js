let URL = "http://127.0.0.1:5000"
let par = /^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9])|(16[0-9]))\d{8}$/
let app = new Vue({
    el: "#app",
    data() {
        return {
            telephone: '',
            password: '',
            show1: true,
            show2: false,
            reg_telephone: '',
            reg_password: '',
            validate_code: '',
            reconfirm_reg_password: '',
            codeStr: "获取验证码",
            codeChange: true,
        }
    },
    methods: {
        login() {
            // if (this.telephone=="nku" && this.password == "123"){
            //     window.location.replace("menu.html");
            // }
            console.log("telephone: " + this.telephone + " password: " + this.password)
            if (this.telephone == null || this.password == null || this.telephone == '' || this.password == '') {
                this.$message({
                    type: "warning",
                    message: '输入不能为空'
                })
            } else if (!(par.test(this.telephone)) || this.telephone.length != 11) {
                this.$message({
                    type: "error",
                    message: '手机号格式有误'
                })
            } else {
                // 发起一个post请求
                console.log("发送登录请求")
                axios({
                    method: 'post',
                    url: URL + '/user',
                    data: {
                        telephone: this.telephone,
                        password: this.password,
                    }
                })
                    .then(resp => {
                        console.log(resp);
                        if (resp.data.flag == true) {
                            this.$message({
                                type:"success",
                                message: resp.data.msg
                            })
                            console.log(resp.data.obj)
                            window.sessionStorage.setItem("id", resp.data.obj);
                            setTimeout(function () {
                                window.location.replace('index.html')
                            }, 400)
                        } else {
                            this.$message({
                                type: "error",
                                message: resp.data.msg
                            })
                        }
                    });
            }
        },
        ToRegister() {
            this.show1 = false;
            setTimeout(() => {
                this.show2 = true;
            }, 500)
        },
        ToLogin() {
            this.show2 = false;
            setTimeout(() => {
                this.show1 = true;
            }, 500)
        },
        isEmpty(e) {
            if (e === null || e === "") {
                return true
            } else {
                return false
            }
        },
        getCode() {
            if (this.codeChange) {
                if (this.isEmpty(this.reg_telephone)) {
                    this.$message({
                        type: "warning",
                        message: '请输入手机号'
                    })
                } else if (!(par.test(this.reg_telephone))) {
                    this.$message({
                        type: "error",
                        message: '手机号格式不正确'
                    })
                } else {
                    console.log("发送请求")
                    axios({
                        method: 'post',
                        url: URL + '/val',
                        data:{ 
                            telephone: this.reg_telephone
                        },
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then(resp => {
                            console.log(resp)
                            if (resp.data.flag == true) {
                                let n = 59;
                                console.log("发送验证码")
                                this.codeChange = false;
                                let time = setInterval(() => {
                                    let str = '(' + n + ')' + '重新获取';
                                    this.codeStr = str;
                                    if (n <= 0) {
                                        this.codeChange = true;
                                        this.codeStr = '重新获取';
                                        clearInterval(time);
                                    }
                                    n--;
                                }, 1000);
                                this.$message({
                                    type: "success",
                                    message: '验证码已发送'
                                })
                            } else {
                                this.$message({
                                    type: "warning",
                                    message: resp.data.msg,
                                })
                            }
                        })
                }
            } else {
                this.$message({
                    type: "warning",
                    message: '请等候重新发送'
                })
            }
        },
        register() {
            if (this.isEmpty(this.reg_telephone) || this.isEmpty(this.reg_password) ||
                this.isEmpty(this.validate_code) || this.isEmpty(this.reconfirm_reg_password)) {
                this.$message({
                    type: "warning",
                    message: "信息不完整"
                })
            } else if (!(par.test(this.reg_telephone))) {
                this.$message({
                    type: "error",
                    message: '手机号格式不正确'
                })
            } else if (this.reg_password != this.reconfirm_reg_password) {
                this.$message({
                    type: "error",
                    message: '密码不一致'
                })
            } else {
                // 发起一个put请求
                axios({
                    method: 'put',
                    url: URL + '/user',
                    data: {
                        telephone: this.reg_telephone,
                        validate_code: this.validate_code,
                        password: this.reg_password,
                        reconfirm_password: this.reconfirm_reg_password,
                    }
                })
                    .then(resp => {
                        console.log(resp)
                        if (resp.data.flag == true) {
                            this.$message({
                                type: "success",
                                message: resp.data.msg
                            })
                            setTimeout(()=> {
                                this.ToLogin()
                            }, 1000)
                        } else {
                            this.$message({
                                type: 'error',
                                message: resp.data.msg
                            })
                        }
                    });
            }
        }
    }
})