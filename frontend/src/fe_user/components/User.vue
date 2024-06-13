<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%; ">
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">
      我的持仓
    </div>

    <el-table ref="dataTable" v-if="isShow" :data="this.tableData" height="555" :table-layout="'auto'"
            style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
      <el-table-column prop="currency_name" label="外币" sortable></el-table-column>
      <el-table-column prop="amount" label="金额" sortable></el-table-column>
      <el-table-column label="操作">
        <template v-slot="{ row }">
          <el-button @click="handleSellCurrency(row)" type="text">卖出</el-button>
        </template>
      </el-table-column>
    </el-table>


  </el-scrollbar>
</template>

<script>

import { Delete, Edit, Search, Plus, ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, datePickerProps, ElButton } from 'element-plus'
import axios from 'axios'
import { DatePicker } from 'ant-design-vue'
import dayjs from 'dayjs'
import { Chart } from 'chart.js/auto'

export default {
  components: {
    ADatePicker: DatePicker,
  },
  data () {
    return {
      tableData: [{
        currency_id: 0, 
        currency_name: '',
        amount: 0,
      }],
      userId: 0,
      Delete,
      Edit,
      Search,
      Plus,
      ArrowLeft,
      isShow: true,
    }
  },
  created() {
    this.fetchDataFromUrl();
  },
  methods: {
    handleSellCurrency(row) {
      console.log(row)
    },
    fetchDataFromUrl() {
      const url = new URL(window.location);
      const params = new URLSearchParams(url.search);
      this.userId = params.get('user_id')
    },
    async getHolding() {
      this.fetchDataFromUrl()
      this.tableData = []

      await axios.get('/FExchange/user/holding', { params: { person_id: this.userId } })
        .then(response => {
            //console.log(response.data)
            if(response.data.error_num === 0) {
              let datas = response.data.holdings
              datas.forEach(element => {
                element.amount = parseFloat(element.amount).toFixed(2)
                this.tableData.push(element)
              })
            } else {
              ElMessage.error("持仓数据请求错误")
              //console.log(response.data.msg)
            }
        })
    }
  },
  mounted() {
    this.getHolding()
  }
}
</script>