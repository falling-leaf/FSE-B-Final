<template>
  <el-scrollbar height="100%" style="width: 100%;">
    <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
    账户开设
    </div>
  <div style="width:30%;margin:0 auto; padding-top:5vh;">
    <div style="height: 20px"></div>
    <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
      身份证：
      <el-input v-model="identity_card" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
    </div>
    <div style="height: 20px"></div>
    <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
      电话号码：
      <el-input v-model="phone_num" style="width: 12.5vw; margin-left: 1rem" maxlength="20" clearable/>
    </div>
    <div style="height: 20px"></div>
    <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
      密码：
      <el-input v-model="password" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
    </div>
    <div style="height: 20px"></div>
    <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px; ">
      <el-button type="primary" style="margin-left: 57px" @click="openNewAccount"
        :disabled="identity_card.length === 0 || password.length === 0">开设账户</el-button>
    </div>
    <!-- 新建账户对话框 -->
    <el-dialog v-model="openAccountVisible" width = "30%" align-center>
      <div class="accountBox" v-if="openAccountVisible">
        <div style="font-size: 25px; font-weight: bold;">新开设账户ID： {{newAccount.id}}</div>
        <el-divider/>
        <p style = "margin-left: 1vw; font-weight: bold; font-size: 1rem; margin-top: 5px;"><span style="font-weight: bold">余额：￥</span>{{newAccount.balance}}</p>
        <p style = "margin-left: 1vw; font-weight: bold; font-size: 1rem; margin-top: 5px;"><span style="font-weight: bold">定期存款：￥</span>{{newAccount.curDeposit}}</p>
        <p style = "margin-left: 1vw; font-weight: bold; font-size: 1rem; margin-top: 5px;"><span style="font-weight: bold">待定存款：￥</span>{{newAccount.uncreditedDeposit}}</p>
        <p style = "margin-left: 1vw; font-weight: bold; font-size: 1rem; margin-top: 5px;"><span style="font-weight: bold">身份证：</span>{{newAccount.identity_card}}</p>
        <p style="padding: 25px;">
          <el-tag v-if="newAccount.isFrozen">已冻结</el-tag>
          <el-tag v-else>未冻结</el-tag>
          <span style = "padding: 10px"></span>
          <el-tag v-if="newAccount.isLost" style="margin-left: 10px">已挂失</el-tag>
          <el-tag v-else>未挂失</el-tag>
        </p>
      </div>
      <template #footer>
        <el-button type="primary" @click="openAccountVisible=false">
          确认
        </el-button>
      </template>
    </el-dialog>

  </div>
  </el-scrollbar>
</template>

<script>

import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  created() {
    this.fetchDataFromUrl();
  },
  data(){
    return{
      cashierID: 0,
      identity_card: '',
      phone_num: '',
      password: '',
      openAccountVisible: false,
      newAccount:
          {
            id: 3,
            password: '',
            identity_card: '330782200408076216',
            phone_num: '',
            //cardType: '',
            balance: 0.00,
            curDeposit: 0.0,
            uncreditedDeposit: 0.0,
            isFrozen: false,
            isLost: false
          }
    }
  },
  methods:{
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);

      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);

      // 从查询字符串中获取参数
      this.cashierID = params.get('cashierID');
    },
    openNewAccount(){
      this.newAccount.identity_card = this.identity_card;
      this.newAccount.password = this.password;
      this.newAccount.phone_num = this.phone_num;
      axios.post('/cashier/add/', {
        identity_card: this.newAccount.identity_card,
        phone_num: this.newAccount.phone_num,
        password: this.newAccount.password,
        cashierID: this.cashierID
      }).then(response => {
        ElMessage.success(response.data.success)
        this.openAccountVisible = true
        this.newAccount.id = response.data.id
      }).catch(error => {
        ElMessage.error(error.response.data.error);
        this.openAccountVisible = false
      })
    }
  }
}
</script>

<style scoped>
.accountBox {
  height:270px;
  width: 300px;
  /* box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19); */
  text-align: center;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
</style>