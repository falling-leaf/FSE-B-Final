<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">
      <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
        互联网个人银行
      </div>
      <div style="display: flex;flex-direction: row">
        <el-card style="width: 60%;margin:20px;padding-left: 40px">
          <div style="">
                <p style="font-size: 30px;font-weight: bolder;margin: 5px;padding: 5px">国内转账</p>
                <el-divider />
                <el-form label-position="right" >
                  <el-form-item label="转出卡号">
                    <el-input style="width: 200px" v-model="toTransferInfo.account_out_id">
                    </el-input>
                  </el-form-item >
                  <el-form-item label="密码" >
                    <el-input style="width: 200px" v-model="toTransferInfo.password" >
                    </el-input>
                  </el-form-item>
                  <el-form-item label="转入卡号">
                    <el-input style="width: 200px" v-model="toTransferInfo.account_in_id" >
                    </el-input>
                  </el-form-item>
                  <el-form-item label="转账金额">
                    <el-input style="width: 200px" v-model="toTransferInfo.transfer_amount" >
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" :disabled="
                    toTransferInfo.transfer_amount.length === 0
                    ||toTransferInfo.account_in_id.length ===0
                    ||toTransferInfo.account_out_id.length ===0
                    ||toTransferInfo.password.length === 0"
                               @click="ConfirmTransfer" >确认</el-button>
                  </el-form-item>
                </el-form>
          </div>
        </el-card>
        <el-card style="margin:20px;padding-left: 40px">
          <div style="">
            <p style="font-size: 30px;font-weight: bolder;margin: 5px;padding: 5px">其他功能</p>
            <el-divider />
            <div>
                  <el-button type="primary"  style="font-size: 20px;margin: 10px;padding: 5px">[ 外汇 ] 国际转账</el-button>
            </div>
            <div style="">
                  <el-button type="primary"  style="font-size: 20px;margin: 10px;padding: 5px" @click="ConfirmLoan">[ 贷款 ] 贷款申请  </el-button>
            </div>
<!--            <a href="/credit_user?online_user_id=this.user_id">-->
            <a>
              <el-button type="primary" style="font-size: 20px;margin: 10px;padding: 5px" @click="ConfirmCreditcard">
                [ 信用卡 ] 信用卡
              </el-button>
            </a>
          </div>
        </el-card>
      </div>
  
    </el-scrollbar>
  </template>
  <script>

  import axios from "axios";
  import {ElMessage} from "element-plus";

  export default {
    data() {
      return {
        user_id:'',
        toTransferInfo:{
          account_out_id:"",
          password:"",
          account_in_id:"",
          transfer_amount:0,
        }
      }
    },
    methods:{
      fetchDataFromUrl() {
        // 获取当前URL
        const url = new URL(window.location);
        console.log(url);  // Use console.log instead of print
        // 创建URLSearchParams对象
        const params = new URLSearchParams(url.search);
        console.log(Array.from(params.entries()));  // Log all parameters to see what is available

        // 从查询字符串中获取参数
        this.user_id = params.get('user_id');
        console.log('User ID:', this.user_id);  // Check if user_id is retrieved correctly
    },

      ConfirmTransfer(){
        axios.post("http://127.0.0.1:8000/user/money_transfer/",{
          account_out_id :this.toTransferInfo.account_out_id,
          account_in_id :this.toTransferInfo.account_in_id,
          password :this.toTransferInfo.password,
          transfer_amount :parseFloat(this.toTransferInfo.transfer_amount)
        }).then(response=>{
          ElMessage.success(response.data.success)
        }).catch(error=>{
          ElMessage.error(error.response.data.error)
        })
      },
      ConfirmLoan(){
        this.fetchDataFromUrl();
        window.location.href =
            "/loan_user?user_id=" + this.user_id ; // 函数内部进行超链接跳转
      },
      ConfirmCreditcard(){
        this.fetchDataFromUrl();
        window.location.href =
            "/credit_user?user_id=" + this.user_id ; // 函数内部进行超链接跳转
      },
    },
    mounted() {
    }
  }

  </script>
  
  <style scoped>

  </style>