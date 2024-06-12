<template>
  <el-scrollbar height="100%" style="width: 100%;">
    <!-- 标题 -->
    <div class="header">
      查询贷款记录
    </div>

    <!-- 查询操作 -->
    <div class="search-bar">
      <el-input v-model="toQuery" placeholder="输入银行卡号" style="width: 15vw; min-width: 150px; margin-right: 20px;"/>
      <el-select v-model="status" placeholder="选择贷款状态" style="width: 15vw; min-width: 150px; margin-right: 20px;">
        <el-option label="所有状态" value=""></el-option>
        <el-option label="审批拒绝" value="审批拒绝"></el-option>
        <el-option label="拒绝放款" value="拒绝放款"></el-option>
        <el-option label="已还款" value="已还款"></el-option>
        <el-option label="待还款" value="待还款"></el-option>
        <el-option label="待放款" value="待放款"></el-option>
        <el-option label="待审批" value="待审批"></el-option>
      </el-select>
      <el-button type="primary" @click="queryLoans">查询</el-button>
    </div>

    <!-- 贷款记录 -->
    <el-table v-if="isShow" :data="filteredRecords" height="600"
              :default-sort="{ prop: 'loan_record_id', order: 'ascending' }" :table-layout="'auto'"
              style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
      <el-table-column prop="application_id" label="贷款记录ID" sortable/>
      <el-table-column prop="account_id" label="银行卡号" sortable/>
      <el-table-column prop="amount" label="贷款金额"/>
      <el-table-column prop="application_data" label="贷款日期"/>
      <el-table-column prop="status" label="状态"/>
    </el-table>
  </el-scrollbar>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      isShow: true,
      records: [],
      status: '',
      toQuery: '',
      userID: '12345' // 示例 person_id
    };
  },
  computed: {
    filteredRecords() {
      return this.records.filter(record => {
        return (this.status === '' || record.status === this.status) &&
            (this.toQuery === '' || record.account_id.toString().includes(this.toQuery));
      });
    }
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);
      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);
      // 从查询字符串中获取参数
      this.userID = params.get('userID');
    },
    queryLoans() {
      axios.post('/loan/searchAllLoanApplicationByUser/', {
        identity_card: "330204197508260578",
      })
          .then(response => {
            let records = response.data.loan_application_list;
            console.log(response.data);
            records.forEach(record => {
              this.records.push(record);
            });
          })
          .catch(error => {
            console.error('There was an error!', error);
            ElMessage.error("查询贷款记录失败");
          });
    },
    remindUnrepayLoan() {
      axios.post('/loan/unrepayLoanRecordReminder/', {
        identity_card: "330204197508260578",
      })
          .then(response => {
            if (response.data.response_code === 1) {
              ElMessage.success(response.data.response_message);
            } else {
              ElMessage.error(response.data.response_message);
            }
          })
          .catch(error => {
            console.error('There was an error!', error);
            ElMessage.error("还款提醒失败");
          });
    }
  },
  mounted() {
    this.queryLoans();
    this.remindUnrepayLoan(); // 页面加载时自动提醒还款
  },
  created() {
    this.fetchDataFromUrl();
  }
};
</script>

<style scoped>
.header {
  margin-top: 20px;
  margin-left: 40px;
  font-size: 2em;
  font-weight: bold;
}

.search-bar {
  margin-top: 20px;
  margin-left: 40px;
  display: flex;
  align-items: center;
}
</style>


