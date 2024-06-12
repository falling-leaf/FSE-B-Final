<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%; ">
    <div style="text-align:center;  margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">  卖出外币
    </div>
    <h1>购买前，请您确保自己的操作合法合规！</h1>
    <h1 class="h11">操作卡号：{{account_id}}</h1>
    <h1 class="h11">外币类型：{{ name }}</h1>
    <h1 class="h11">发行国家：{{ country }}</h1>
    <el-form ref="form" label-width="100px">
      <el-form-item label="卖出数量：" size="large">
        <el-input-number v-model="rmb_account" placeholder="二位精确" value-on-clear="min" min=0.00 step=0.01></el-input-number>
      </el-form-item>
    </el-form>
    <h1 class="h11">当前卖出价：{{ price }}</h1>
    <h1 class="h11">预计收益：{{ rmb_account*price }}</h1>
    <el-button class="but" @click="UpdateSellHistory">确定</el-button>
    <el-button class="but" @click="GoBack">取消</el-button>
  </el-scrollbar>
</template>

<script >
import {ref} from "vue"
import {Delete, Edit, Plus, Search} from "@element-plus/icons-vue";
import {message} from "ant-design-vue";
import axios from "axios";

export default {
  data() {
    return {
      account_id: "0000000000000000",
      isme: false,
      rmb_account: 0.00,
      buy_or_sell: false,
      isShow: true,
      isDisplaySearchBox: false,
      curPage: 0,
      Edit,
      Delete,
      Search,
      Plus,
      name: "Default",
      country: "Default",
      price: 2.00,
      selectedRowData: null,
    }
  },
  methods: {
    GoBack() {
      this.$router.push('/FExchange/user/currency')
    },
    GetCurrency() {

    },
    async UpdateSellHistory() {
      try{const response = await axios.post('/FExchange/user/currency/sell',{"account_id":this.account_id,
        "rmb_amount":this.rmb_account,
        "currency_amount":this.rmb_account*this.price,
      });
      if (response.status === 200) {
        // 请求成功，根据实际情况处理成功的逻辑
        alert('交易成功');
        this.$router.push('/FExchange/user/currency');
        // 可能还需要更新页面数据等操作
      } else {
        // 请求失败，根据实际情况处理失败的逻辑
        alert('交易失败，请重试');
        // 可能需要提示用户或者执行其他操作
      }
    } catch (error) {
      // 捕获异常并进行处理
      console.error("请求异常：", error);
      // 可能需要提示用户或者执行其他操作
    }
    }
  }
}
</script>

<style>
.h11{
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