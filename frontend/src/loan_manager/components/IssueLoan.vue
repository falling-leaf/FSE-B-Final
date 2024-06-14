<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <!--贷款申请信息显示卡片-->
    <div style="margin-left:20px; display: flex; flex-wrap: wrap; justify-content: start;">
      <div class="loanBox" v-for="loan in loans" :key="loan.approval_id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">批准的贷款编号: {{ loan.approval_id }}</div>

          <el-divider />

          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2.5px;"><span style="font-weight: bold">身份证：</span>{{ loan.identity_card }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">银行卡号：</span>{{ loan.account_id }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">批准贷款金额：</span>{{ loan.amount }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">贷款期限：</span>{{ loan.loan_duration }}</p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-left: 5px; margin-top: -20px; display: flex; justify-content: space-between;">
            <el-button type="success" @click="approveLoan(loan.approval_id)">发放</el-button>
            <el-button type="danger" @click="rejectDisburseLoan(loan.approval_id)">拒绝</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 贷款通过对话框 -->
    <el-dialog v-model="loanApprovalVisible" title="是否发放该用户申请的贷款" width="30%" align-center>

      <!-- 底部按钮 -->
      <template #footer>
        <span>
          <el-button @click="loanApprovalVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmLoanApproval">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 贷款拒绝对话框 -->
    <el-dialog v-model="loanRejectionVisible" title="是否拒绝发放该用户申请的贷款" width="30%" align-center>

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
      loans: [],
      loanApprovalVisible: false,
      loanRejectionVisible: false,
      loan_manager_id: 0,
      currentLoan: {
        approval_id: 2,
        loan_manager_id: 1, // Assuming the loan manager ID is 1 for demonstration
        result: '',
      }
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
      this.loan_manager_id = params.get('loan_manager_id');
    },
    approveLoan(approval_id) {
      this.currentLoan = this.loans.find(loan => loan.approval_id === approval_id);
      this.currentLoan.result = 'True';
      this.loanApprovalVisible = true;
    },
    rejectDisburseLoan(approval_id) {
      this.currentLoan = this.loans.find(loan => loan.approval_id === approval_id);
      this.currentLoan.result = 'False';
      this.loanRejectionVisible = true;
    },
    confirmLoanApproval() {
      axios.post('/loanManager/lenderLoanApplication/', {
        "loan_manager_id": this.loan_manager_id,
        "result": this.currentLoan.result,
        "approval_id": this.currentLoan.approval_id,
      })
          .then(response => {
            if(response.data.response_code === 1){
            ElMessage.success("贷款已发放");
            this.loanApprovalVisible = false;
            this.queryLoans();
          }else{
            ElMessage.error("贷款发放失败");
          }
          })
          .catch(error => {
            ElMessage.error("贷款发放失败");
          });
    },
    confirmLoanRejection() {
      axios.post('/loanManager/lenderLoanApplication/', this.currentLoan)
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
    queryLoans() {
    this.loans = [];
      axios.get('/loanManager/showAllLoanApplicationUnlent/')
          .then(response => {
            if(response.data.response_code === 1){
            let loans = response.data.unlent_approval_list
            ElMessage.success("查询贷款记录成功");
            loans.forEach(loan => {
              this.loans.push(loan)
            })
          }else{
            ElMessage.error("查询贷款记录失败");
          }
          })
          .catch(error => {
            ElMessage.error("查询贷款记录失败");
          });
    },
    remindUnrepayLoan() {
      axios.get('/loanManager/unrepayReminderManager/')
          .then(response => {
            if (response.data.response_code === 1) {
              ElMessage.success(response.data.response_message);
            } else {
              ElMessage.error(response.data.response_message);
            }
          })
          .catch(error => {
            ElMessage.error("还款提醒失败");
          });
    }
  },
  mounted() {
    this.remindUnrepayLoan(); // 页面加载时自动提醒还款
    this.queryLoans();
  }
}
</script>

<style scoped>
.loanBox {
  height: 330px;
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



