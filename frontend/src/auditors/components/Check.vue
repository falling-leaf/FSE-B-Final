<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <!--贷款申请信息显示卡片-->
    <div style="margin-left:20px; display: flex; flex-wrap: wrap; justify-content: start;">
      <div class="loanBox" v-for="record in records" :key="record.application_id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">申请编号: {{ record.application_id }}</div>

          <el-divider />

          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2.5px;"><span style="font-weight: bold">身份证：</span>{{ record.identity_card }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">银行卡号：</span>{{ record.account_id }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">贷款金额：</span>{{ record.amount }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">贷款期限：</span>{{ record.loan_duration }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">贷款日期：</span>{{ record.application_data }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">信用额度：</span>{{ record.credit_limit }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">当前已贷款未还数量：</span>{{ record.lent_money }}</p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-left: 5px; margin-top: -20px; display: flex; justify-content: space-between;">
            <el-button type="success" @click="approveLoan(record.application_id)">批准</el-button>
            <el-button type="danger" @click="rejectLoan(record.application_id)">拒绝</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 贷款通过对话框 -->
    <el-dialog v-model="loanApprovalVisible" title="是否批准该用户申请的贷款" width="30%" align-center>
      <!-- 底部按钮 -->
      <template #footer>
        <span>
          <el-button @click="loanApprovalVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmLoanApproval">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 贷款拒绝对话框 -->
    <el-dialog v-model="loanRejectionVisible" title="是否拒绝该用户申请的贷款" width="30%" align-center>
      <!-- 底部按钮 -->
      <template #footer>
        <span>
          <el-button @click="loanRejectionVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmLoanRejection">确定</el-button>
        </span>
      </template>
    </el-dialog>

  </el-scrollbar>
</template>

<script>
import axios from "axios";
import { ElMessage } from 'element-plus'
export default {
  data() {
    return {
      auditor_id:0,
      records: [],
      loanApprovalVisible: false,
      loanRejectionVisible: false,
      currentLoan: {},
    }
  },
  created() {
    this.fetchDataFromUrl();
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);

      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);

      // 从查询字符串中获取参数
      this.auditor_id = params.get('auditor_id');
    },
    approveLoan(application_id) {
      this.currentLoan = this.records.find(record => record.application_id === application_id);
      this.loanApprovalVisible = true;
    },
    rejectLoan(application_id) {
      this.currentLoan = this.records.find(record => record.application_id === application_id);
      this.loanRejectionVisible = true;
    },
    confirmLoanRejection() {
      axios.post('/loanExaminer/approvalLoanApplication/', {
            "result": "False",
            "loan_examiner_id": this.auditor_id,
            "application_id": this.currentLoan.application_id,
      })
          .then(response => {
            if(response.data.response_code === 1){
            ElMessage.success("贷款已拒绝");
            this.loanRejectionVisible = false;
            this.queryLoans();
          }else{
            ElMessage.error("贷款拒绝失败");
          }
          })
          .catch(error => {
            ElMessage.error("贷款拒绝失败");
          });
    },
    confirmLoanApproval() {
      axios.post('/loanExaminer/approvalLoanApplication/', {
            "result": "True",
            "loan_examiner_id": this.auditor_id,
            "application_id": this.currentLoan.application_id,
      })
          .then(response => {
            if(response.data.response_code === 1){
            ElMessage.success("贷款已批准");
            this.loanApprovalVisible = false;
            this.queryLoans();
          }else{
            ElMessage.error("贷款批准失败");
          }
          })
          .catch(error => {
            ElMessage.error("贷款批准失败");
          });
    },
    queryLoans() {
    this.records = [];
      axios.get('/loanExaminer/showAllLoanApplicationUnapproved/')
          .then(response => {
            if(response.data.response_code === 1){
            let records = response.data.unapproved_application_list
            ElMessage.success("查询贷款记录成功");
            records.forEach(record => {
              this.records.push(record)
            })
          }else{
            ElMessage.error("查询贷款记录失败");
          }
          })
          .catch(error => {
            ElMessage.error("查询贷款记录失败");
          });
    }
  },
  mounted() {
    this.queryLoans();
  }
}
</script>

<style scoped>
.loanBox {
  height: 400px;
  width: 300px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
</style>


