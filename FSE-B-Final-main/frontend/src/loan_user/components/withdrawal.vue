<template>
  <el-scrollbar height="100%" style="width: 100%;">
    <!-- 标题和搜索框 -->
    <div class="header">
      账户还款
      <el-input v-model="toSearch" :prefix-icon="Search"
                style="width: 15vw; min-width: 150px; margin-left: 30px; margin-right: 30px; float: right;"
                clearable />
    </div>

    <!-- 还款操作 -->
    <div class="actions">
      <el-button type="primary"  style="margin-left: 10px;" @click="repaymentVisible = true">申请还款</el-button>
    </div>

    <!-- 贷款记录 -->
    <el-table v-if="isShow" :data="fitlerTableData" height="600"
              :default-sort="{ prop: 'application_id', order: 'ascending' }" :table-layout="'auto'"
              style="width: 100%; margin: 30px 50px; max-width: 80vw;">
      <el-table-column prop="loan_id" label="贷款记录ID" sortable/>
      <el-table-column prop="account_id" label="银行卡号" sortable/>
      <el-table-column prop="amount" label="贷款金额"/>
      <el-table-column prop="end_time" label="贷款截止日期"/>
    </el-table>

    <el-dialog v-model="repaymentVisible" title="申请还款" width="30%" align-center>
      <div class="form-group">
        <label>身份证号：</label>
        <el-input v-model="newRepaymentInfo.identity_card" clearable/>
      </div>
      <div class="form-group">
        <label>银行卡号(用于还款的银行卡)：</label>
        <el-input v-model="newRepaymentInfo.account_id" clearable/>
      </div>
      <div class="form-group">
        <label>需要还款的记录编号：</label>
        <el-input v-model="newRepaymentInfo.loan_id" clearable/>
      </div>

      <template #footer>
        <span>
          <el-button @click="repaymentVisible = false">取消</el-button>
          <el-button type="primary" @click="setNewRepayment"
                     :disabled="newRepaymentInfo.account_id.length === 0">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>

<script>
import axios from 'axios';
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      isShow: false, // 结果表格展示状态
      records: [], // 还款记录
      repaymentVisible: false,
      Search,
      toSearch: '', // 搜索内容
      newRepaymentInfo: { // 待新建还款信息
        identity_card:'',
        account_id: '',
        loan_id : 0
      },
      userID: ''
    }
  },
  computed: {
    fitlerTableData() { // 搜索规则
      return this.records.filter(
          (tuple) =>
              (this.toSearch === '') || // 搜索框为空，即不搜索
              tuple.application_id === this.toSearch  // 图书号与搜索要求一致
      )
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
    //查询所有需要还款的记录
    queryRepayments() {
      axios.post('/loan/searchAllNeedRepayLoanRecord/', {
            identity_card: "330204197508260578",
      })
          .then(response => {
            let records = response.data.loan_application_list
            console.log(response.data)
            records.forEach(record => {
              this.records.push(record)
            })
          })
          .catch(error => {
            console.error('There was an error!', error);
            // 可以在这里处理错误，例如显示错误消息
          });
          this.isShow = true;
    },
    //repay还款
    setNewRepayment() {
      axios.post("/loan/userRepayLoanByAccount/", {
        // 请求体
        account_id: this.newRepaymentInfo.account_id,
        identity_card: this.newRepaymentInfo.identity_card,
        loan_id: this.newRepaymentInfo.loan_id
      })
          .then(response => {
            ElMessage.success("还款成功"); // 显示消息提醒
            this.repaymentVisible = false; // 将对话框设置为不可见
            this.queryRepayments(); // 重新查询还款记录以刷新页面
          })
          .catch(error => {
            console.error('There was an error!', error);
            ElMessage.error("还款失败");
          });

      this.newRepaymentInfo = {
        identity_card: '',
        account_id: '',
        loan_id: 0
      };
    },
  },
  mounted() {
    this.queryRepayments(); // 查询还款记录
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

.actions {
  width: 30%;
  margin-left: 30px;
  padding-top: 5vh;
}

.form-group {
  margin-left: 2vw;
  font-weight: bold;
  font-size: 1rem;
  margin-top: 20px;
}
</style>
