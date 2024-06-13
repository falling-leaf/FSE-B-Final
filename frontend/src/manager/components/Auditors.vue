<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <!--贷款审核员信息显示卡片-->
    <div style="margin-left:20px; display: flex; flex-wrap: wrap; justify-content: start;">
      <div class="examinerBox" v-for="examiner in examiners" :key="examiner.loan_examiner_id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">No. {{examiner.loan_examiner_id}}</div>
          <el-divider />
          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2.5px;"><span style="font-weight: bold">员工ID：</span>{{examiner.employee_id}}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">账户名：</span>{{examiner.account}}</p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-top: 10px; margin-left: 0; display:flex">
            <el-button type="primary" @click="this.modPasswordExaminerVisible = true, this.modPasswordExaminerInfo.loan_examiner_id = examiner.loan_examiner_id">
              修改密码
            </el-button>
            <el-button type="danger" @click="this.deleteExaminerID = examiner.loan_examiner_id, this.deleteExaminerVisible = true">
              删除
            </el-button>
          </div>
        </div>
      </div>
      <el-button class="newExaminerBox" @click="newExaminerVisible = true, newExaminerInfo.employee_id = '', newExaminerInfo.account = '', newExaminerInfo.password = ''">
        <el-icon style="height: 50px; width: 50px;">
          <Plus style="height: 100%; width: 100%;" />
        </el-icon>
      </el-button>
    </div>

    <!--添加贷款审核员对话框-->
    <el-dialog v-model="newExaminerVisible" title="添加贷款审核员" width="30%" align-center>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        雇员ID：
        <el-input v-model="newExaminerInfo.employee_id" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable />
      </div>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        账户名：
        <el-input v-model="newExaminerInfo.account" style="width: 12.5vw; margin-left: 1rem" maxlength="20" clearable/>
      </div>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        密码：
        <el-input type="password" v-model="newExaminerInfo.password" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable/>
      </div>
      <!--底部按钮-->
      <template #footer>
        <span>
          <el-button @click="newExaminerVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmNewExaminer"
                     :disabled="newExaminerInfo.employee_id.length === 0 || newExaminerInfo.account.length === 0 || newExaminerInfo.password.length === 0">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改贷款审核员密码对话框 -->
    <el-dialog v-model="modPasswordExaminerVisible" title="修改贷款审核员密码" width="30%" align-center>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        新密码：
        <el-input type="password" v-model="modPasswordExaminerInfo.new_password" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable/>
      </div>
      <!--底部按钮-->
      <template #footer>
        <span>
          <el-button @click="modPasswordExaminerVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmModPasswordExaminer"
                     :disabled="modPasswordExaminerInfo.new_password.length === 0">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除贷款审核员确认框 -->
    <el-dialog v-model="deleteExaminerVisible" title="删除贷款审核员" width="30%">
      <span>确定删除<span style="font-weight: bold;">{{ deleteExaminerID }}号贷款审核员</span>吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteExaminerVisible = false">取消</el-button>
          <el-button type="danger" @click="ConfirmDeleteExaminer">删除</el-button>
        </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>

<script>
import axios from "axios";
import { ElMessage } from 'element-plus'
export default{
  data(){
    return{
      examiners: [],
      newExaminerVisible: false,
      newExaminerInfo: {
        employee_id: 0,
        account: '',
        password: ''
      },
      modPasswordExaminerVisible: false,
      modPasswordExaminerInfo: {
        loan_examiner_id: 0,
        new_password: ''
      },
      deleteExaminerVisible: false,
      deleteExaminerID: 0
    }
  },
  methods: {
    ConfirmNewExaminer() {
      axios.post('/manager/manage_loan_examiner/', {
        operation: "add",
        employee_id: this.newExaminerInfo.employee_id,
        account: this.newExaminerInfo.account,
        password: this.newExaminerInfo.password
      })
          .then(response => {
            ElMessage.success(response.data.response_message)
            this.newExaminerVisible = false
            this.QueryExaminers()
          })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    ConfirmModPasswordExaminer() {
      axios.post('/manager/manage_loan_examiner/', {
        operation: "update",
        loan_examiner_id: this.modPasswordExaminerInfo.loan_examiner_id,
        new_password: this.modPasswordExaminerInfo.new_password
      }).then(response => {
        ElMessage.success(response.data.response_message)
        this.modPasswordExaminerVisible = false
        this.QueryExaminers()
      })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    ConfirmDeleteExaminer() {
      axios.post('/manager/manage_loan_examiner/', {
        operation: "delete",
        loan_examiner_id: this.deleteExaminerID
      }).then(response => {
        ElMessage.success(response.data.response_message)
        this.deleteExaminerVisible = false
        this.QueryExaminers()
      })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    QueryExaminers() {
      this.examiners = [
        {
          loan_examiner_id: 1,
          employee_id: 101,
          account: 'examiner1'
        },
        {
          loan_examiner_id: 2,
          employee_id: 102,
          account: 'examiner2'
        },
        {
          loan_examiner_id: 3,
          employee_id: 103,
          account: 'examiner3'
        }
      ]
      axios.post('/manager/getAllLoanExaminer/', {
        operation: "get"
      })
          .then(response => {
            let examiners = response.data.examiners;
            console.log(response.data);
            examiners.forEach(examiner => {
              this.examiners.push(examiner);
            });
          })
      .catch(error => {
        ElMessage.error(error.response.data.response_message)
      })
    }
  },
  mounted() {
    this.QueryExaminers()
  }
}
</script>

<style scoped>
.examinerBox {
  height: 250px;
  width: 275px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
.newExaminerBox {
  height: 250px;
  width: 275px;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}
</style>

