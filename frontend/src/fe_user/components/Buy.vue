<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%; text-align: center;">
    <div style="margin-top: 20px; font-size: 2em; font-weight: bold; ">买入外币</div>
      <div style="font-size: 1em; margin-top: 20px;">购买前，请您确保自己的操作合法合规！</div>
      <el-select v-model="this.selected_account_id" placeholder="请选择卡号" style="width: 300px; margin-top: 20px;" >
        <el-option v-for="option in options" :key="option.value" :label="option.label" :value="option.value"></el-option>
      </el-select>
      <div style="font-size: 1em; margin-top: 20px;">外币类型：{{ this.currency_name }}</div>
      <div style="font-size: 1em; margin-top: 20px;">您当前持有：{{ this.fix2(this.current) }}</div>
      <div style="font-size: 1em; margin-top: 20px;">买入数量：
        <el-input-number v-model="this.currency_amount" placeholder="二位精确" value-on-clear="min" min=0.00 step=0.01></el-input-number>
      </div>
      <div style="font-size: 1em; margin-top: 20px;">当前现汇卖出价：{{ this.price }}</div>
      <div style="font-size: 1em; margin-top: 20px;">预计花费：{{ this.fix2(this.currency_amount/100*this.price)  }}</div>
      <div style="font-size: 1em; margin-top: 20px;"></div>
      <el-button class="but" @click="inputPassword">确定</el-button>
      <el-button class="but" @click="GoBack">取消</el-button>

      <el-dialog v-model="isInputPassword" :title="'搜索条件'" width="30%"
        align-center>

        <div
          style="
            margin-left: 4.3vw;
            font-weight: bold;
            font-size: 1rem;
            margin-top: 5px;
          ">
          密码：
        <el-input
          v-model="password"
          style="width: 12.5vw; margin-left: 1rem"
          type="password"
          maxlength="20"
          clearable
        /></div>

        <template #footer>
          <span class="dialog-footer">
            <el-button @click="confirmTransaction">确认</el-button>
            <el-button @click="isInputPassword = false">取消</el-button>
          </span>
        </template>
      </el-dialog>

  </el-scrollbar>
</template>

<script >
import {ref} from "vue"
import {Delete, Edit, Plus, Search} from "@element-plus/icons-vue";
import {message} from "ant-design-vue";
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      selected_account_id: "", // 用于绑定选中的卡号
      options: [{
        label: '',
        value: '',
      }],
      isme: false,
      currency_amount: 0.00,
      buy_or_sell: false,
      isShow: true,
      isDisplaySearchBox: false,
      current: 0,
      Edit,
      Delete,
      Search,
      Plus,
      dialogVisible: false, // 控制对话框显示
      password: '' ,// 密码输入框绑定的变量
      currency_name: "",
      price: 2.00,
      selectedRowData: null,
      userId: 1,
      isInputPassword: false,
      password: "",
      account: "",//写一个获取account
    }
  },
  mounted() {
    this.GetCurrency();
    this.getAllAccount()
    this.getUserAccountName()
  },
  created() {
    this.fetchDataFromUrl();
  },
  methods: {
    fix2(number) {
      return parseFloat(number).toFixed(2)
    },
    inputPassword() {
      if(this.selected_account_id === "") {
        ElMessage.warning("请选择卡号")
        return
      }
      this.isInputPassword = true
    },
    confirmTransaction() {
      axios.post("http://127.0.0.1:8000/user/sign_in/", {
          user_name: this.account,
          password: this.password,
        })
        .then((response) => {
          this.UpdateAccount()
          this.UpdateBuyHistory()
          this.UpdateHoldings()
          this.GoBack()
          this.isInputPassword = false
        })
        .catch((error) => {
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
    GoBack() {
      this.$router.push('/FExchange/user/currency?user_id=' + this.userId)
    },
    fetchDataFromUrl(){
      const url = new URL(window.location);
      const params = new URLSearchParams(url.search);
      this.currency_name = params.get('currency_name');
      this.userId = params.get('user_id')
    },
    async GetCurrency(){
      this.fetchDataFromUrl()
      let queryParams = {}
      if(this.selectedRowData != '') {
        queryParams.currency_name = this.currency_name
      } 

      if(this.userId != 0) {
        queryParams.person_id = this.userId
      } 
      this.current = 0
      await axios.get('/FExchange/user/currency/amount', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            let holdings = response.data.holdings
            holdings.forEach(element => {
              this.current = element.amount
            })
          } else {
            ElMessage.error("搜索请求错误")
          }
      })

      await axios.get('/FExchange/user/currency/rate', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            let rates = response.data.rates
            rates.forEach(element => {
              this.price = element.selling_rate
            })
          } else {
            ElMessage.error("汇率请求错误")
          }
      })
    },
    async getAllAccount() {
      this.fetchDataFromUrl()
      this.options = []
      let queryParams = {}
      if(this.userId != 0) {
        queryParams.user_id = this.userId
      } 

      await axios.get('/FExchange/user/account', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            let datas = response.data.data
            datas.forEach(element => {
              this.options.push(element)
            })
          } else {
            ElMessage.error("卡号列表请求错误")
            //console.log(response.data.msg)
          }
        })
    },
    async UpdateBuyHistory() {
      this.fetchDataFromUrl()
      let queryParams = {}
      queryParams.user_id = this.userId
      queryParams.currency_name = this.currency_name
      queryParams.buy_or_sell = 1
      queryParams.account_id = this.selected_account_id
      queryParams.rmb_amount = this.currency_amount/100*this.price
      queryParams.currency_amount = this.currency_amount
      //console.log(queryParams)

      await axios.post('/FExchange/history/add', queryParams)
        .then(response => {
          //console.log(response.data);
          if (response.data.status === 'success') {
            //ElMessage.success('Currency add successfully');
          } else {
            //alert('Error: ' + response.data.message);
          }
        })
        .catch(error => {
          //ElMessage.warning('添加请求发送失败', error);
        });
    },
    async UpdateHoldings() {
      this.fetchDataFromUrl()
      let queryParams = {}
      queryParams.user_id = this.userId
      queryParams.currency_name = this.currency_name
      queryParams.currency_amount = parseFloat(this.current) + parseFloat(this.currency_amount)
      //console.log(queryParams)

      await axios.get('/FExchange/user/currency_holding/update', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            ElMessage.success("成功买入")
          } else {
            //ElMessage.error("卡号列表请求错误")
          }
        })
    },
    async UpdateAccount() {
      let queryParams = {}
      queryParams.account_id = this.selected_account_id
      queryParams.rmb_amount = this.currency_amount/100*this.price
      queryParams.password = this.password

      await axios.get('/FExchange/user/account/buy', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            //console.log("yes")
          } else {
            //console.log(response.data.msg)
          }
        })
    },
    async getUserAccountName() {
      let queryParams = {}

      queryParams.user_id = this.userId

      await axios.get('/FExchange/user/getname', { params: queryParams })
        .then(response => {
          if(response.data.error_num === 0) {
            this.account = response.data.name
            //console.log(this.account)
          } else {
            //console.log(response.data.msg)
          }
        })
    },
  }
}
</script>

<style>
.div1{
  margin-left: 110px;
  color: #222222;
  font-size: medium;
  margin-top:30px;
  margin-bottom: 30px;
}
.but{
  margin-left: 60px;
  color: aqua;
  margin-right: 60px;
}
</style>