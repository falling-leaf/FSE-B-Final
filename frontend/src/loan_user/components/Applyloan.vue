<template>
  <el-scrollbar height="100%" style="width: 100%;">
    <!-- 标题和搜索框 -->
    <div class="header">
      账户贷款
      <el-input v-model="toSearch" :prefix-icon="Search"
                style="width: 15vw; min-width: 150px; margin-left: 30px; margin-right: 30px; float: right;"
                clearable @input="filterTableData"/>
    </div>

    <!-- 贷款操作 -->
    <div class="actions">
      <el-button type="primary" style="margin-left: 10px;" @click="loanApplicationVisible = true">申请贷款</el-button>
    </div>

    <!-- 贷款记录 -->
    <el-table v-if="isShow" :data="filteredRecords" height="600"
              :default-sort="{ prop: 'loan_record_id', order: 'ascending' }" :table-layout="'auto'"
              style="width: 100%; margin: 30px 50px; max-width: 80vw;">
      <el-table-column prop="application_id" label="贷款记录ID" sortable/>
      <el-table-column prop="account_id" label="银行卡号" sortable/>
      <el-table-column prop="amount" label="贷款金额"/>
      <el-table-column prop="application_data" label="贷款期限"/>
      <el-table-column prop="status" label="当前贷款状态"/>
    </el-table>


    <el-dialog v-model="loanApplicationVisible" title="申请贷款" width="30%" align-center>
      <div class="form-group">
      <label>身份证号：</label>
      <el-input v-model="newLoanInfo.identity_card" clearable/>
      </div>
      <div class="form-group">
        <label>银行卡号：</label>
        <el-input v-model="newLoanInfo.account_id" clearable/>
      </div>
      <div class="form-group">
        <label>贷款金额：</label>
        <el-input-number v-model="newLoanInfo.loan_amount" :precision="2" :step="0.1" clearable/>
      </div>
      <div class="form-group">
        <label>贷款期限：   (月)</label>
        <el-input v-model="newLoanInfo.loan_term" clearable/>
      </div>
      <template #footer>
        <span>
          <el-button @click="loanApplicationVisible = false">取消</el-button>
          <el-button type="primary" @click="applyLoan"
                     :disabled="!isFormValid">确定</el-button>
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
      isShow: true,
      records: [],
      loanApplicationVisible: false,
      Search,
      identity_card: '',
      toSearch: '',
      newLoanInfo: {
        identity_card: '',
        account_id: '',
        loan_amount: 0,
        loan_term: 0,
      },
      user_id:0
    };
  },
  computed: {
    filteredRecords() {
      return this.records.filter(record => {
        return Object.values(record).some(val => String(val).includes(this.toSearch));
      });
    },
    isFormValid() {
      const { account_id, identity_card, loan_amount, loan_term } = this.newLoanInfo;
      return account_id && identity_card && loan_amount && loan_term;
    }
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);
      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);
      // 从查询字符串中获取参数
      this.user_id = params.get('user_id');
    },
    getIdentity_card(){
      axios.post('/login/getUserIdentityCard/', {
        user_id: this.user_id,
      })
          .then(response => {
            this.identity_card = response.data.identity_card
            console.log(response.data.identity_card)
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    //TODO 查询用户贷款记录的接口,展示还未通过的贷款记录
    queryLoans() {
      axios.post('/loan/searchAllLoanApplicationByUser/', {
            identity_card: this.identity_card,
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
          });
    },
    //TODO 用户申请贷款的接口，待实现
    applyLoan() {
      axios.post("/loan/commitLoanApplication/", {
        identity_card: this.newLoanInfo.identity_card,
        account_id: this.newLoanInfo.account_id,
        amount: parseFloat(this.newLoanInfo.loan_amount),
        loan_duration: this.newLoanInfo.loan_term,
      })
          .then(response => {
            ElMessage.success("贷款申请成功");
            this.loanApplicationVisible = false;
            this.queryLoans();
          })
          .catch(error => {
            console.error('There was an error!', error);
            ElMessage.error("贷款申请失败");
          });

      this.newLoanInfo = {
        identity_card: '',
        account_id: '',
        loan_amount: 0,
        loan_term: '',
      };
    },
  },
  //渲染
  mounted() {
    this.queryLoans();
  },
  created() {
    this.fetchDataFromUrl();
    this.getIdentity_card();
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
  width: 70%;
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

