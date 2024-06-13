<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <!--贷款部门经理信息显示卡片-->
    <div style="margin-left:20px; display: flex; flex-wrap: wrap; justify-content: start;">
      <div class="managerBox" v-for="manager in managers" :key="manager.loan_manager_id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">No. {{manager.loan_manager_id}}</div>
          <el-divider />
          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2.5px;"><span style="font-weight: bold">员工ID：</span>{{manager.employee_id}}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">账户名：</span>{{manager.account}}</p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-top: 10px; margin-left: 0; display:flex">
            <el-button type="primary" @click="this.modPasswordManagerVisible = true, this.modPasswordManagerInfo.loan_manager_id = manager.loan_manager_id">
              修改密码
            </el-button>
            <el-button type="danger" @click="this.deleteManagerID = manager.loan_manager_id, this.deleteManagerVisible = true">
              删除
            </el-button>
          </div>
        </div>
      </div>
      <el-button class="newManagerBox" @click="newManagerVisible = true, newManagerInfo.employee_id = '', newManagerInfo.account = '', newManagerInfo.password = ''">
        <el-icon style="height: 50px; width: 50px;">
          <Plus style="height: 100%; width: 100%;" />
        </el-icon>
      </el-button>
    </div>

    <!--添加贷款部门经理对话框-->
    <el-dialog v-model="newManagerVisible" title="添加贷款部门经理" width="30%" align-center>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        雇员ID：
        <el-input v-model="newManagerInfo.employee_id" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable />
      </div>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        账户名：
        <el-input v-model="newManagerInfo.account" style="width: 12.5vw; margin-left: 1rem" maxlength="20" clearable/>
      </div>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        密码：
        <el-input type="password" v-model="newManagerInfo.password" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable/>
      </div>
      <!--底部按钮-->
      <template #footer>
        <span>
          <el-button @click="newManagerVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmNewManager"
                     :disabled="newManagerInfo.employee_id.length === 0 || newManagerInfo.account.length === 0 || newManagerInfo.password.length === 0">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改贷款部门经理密码对话框 -->
    <el-dialog v-model="modPasswordManagerVisible" title="修改贷款部门经理密码" width="30%" align-center>
      <div style="margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        新密码：
        <el-input type="password" v-model="modPasswordManagerInfo.new_password" style="width: 12.5vw; margin-left: 2rem" maxlength="20" clearable/>
      </div>
      <!--底部按钮-->
      <template #footer>
        <span>
          <el-button @click="modPasswordManagerVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmModPasswordManager"
                     :disabled="modPasswordManagerInfo.new_password.length === 0">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除贷款部门经理确认框 -->
    <el-dialog v-model="deleteManagerVisible" title="删除贷款部门经理" width="30%">
      <span>确定删除<span style="font-weight: bold;">{{ deleteManagerID }}号贷款部门经理</span>吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteManagerVisible = false">取消</el-button>
          <el-button type="danger" @click="ConfirmDeleteManager">删除</el-button>
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
      managers: [],
      newManagerVisible: false,
      newManagerInfo: {
        employee_id: 0,
        account: '',
        password: ''
      },
      modPasswordManagerVisible: false,
      modPasswordManagerInfo: {
        loan_manager_id: 0,
        new_password: ''
      },
      deleteManagerVisible: false,
      deleteManagerID: 0
    }
  },
  methods: {
    ConfirmNewManager() {
      axios.post('/manager/manage_loan_department_manager/', {
        operation: "add",
        employee_id: this.newManagerInfo.employee_id,
        account: this.newManagerInfo.account,
        password: this.newManagerInfo.password
      })
          .then(response => {
            ElMessage.success(response.data.response_message)
            this.newManagerVisible = false
            this.QueryManagers()
          })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    ConfirmModPasswordManager() {
      axios.post('/manager/manage_loan_department_manager/', {
        operation: "update",
        loan_manager_id: this.modPasswordManagerInfo.loan_manager_id,
        new_password: this.modPasswordManagerInfo.new_password
      }).then(response => {
        ElMessage.success(response.data.response_message)
        this.modPasswordManagerVisible = false
        this.QueryManagers()
      })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    ConfirmDeleteManager() {
      axios.post('/manager/manage_loan_department_manager/', {
        operation: "delete",
        loan_manager_id: this.deleteManagerID
      }).then(response => {
        ElMessage.success(response.data.response_message)
        this.deleteManagerVisible = false
        this.QueryManagers()
      })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    },
    QueryManagers() {
<<<<<<< HEAD
      axios.get('/manager/getAllLoanManager/')
=======
      this.managers = [
        {
          loan_manager_id: 1,
          employee_id: 301,
          account: 'manager1'
        },
        {
          loan_manager_id: 2,
          employee_id: 302,
          account: 'manager2'
        },
        {
          loan_manager_id: 3,
          employee_id: 303,
          account: 'manager3'
        }
      ]
      axios.post('/manager/getAllLoanManager/')
>>>>>>> 05afb8749b922f86500152ff4be6a959c283c9c9
          .then(response => {
            let managers = response.data.loan_manager_list;
            console.log(response.data);
            managers.forEach(manager => {
              this.managers.push(manager);
            });
          })
          .catch(error => {
            ElMessage.error(error.response.data.response_message)
          })
    }
  },
  mounted() {
    this.QueryManagers()
  }
}
</script>

<style scoped>
.managerBox {
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
.newManagerBox {
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




