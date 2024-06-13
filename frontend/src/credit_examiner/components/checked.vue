<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        信用卡申请单
    </div>

    <!-- 记录 --> 
    <el-table :data="tableData" height="600" stripe
        :default-sort="{ prop: 'apply_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
        <el-table-column prop="apply_id" label="序号" sortable width="100"/>
        <el-table-column prop="apply_date" label="申请时间" sortable width="200"/>
        <el-table-column prop="account_id" label="申请人ID" width="140"/>
        <el-table-column prop="credit" label="信誉" width="140"/>
        <el-table-column prop="examiner_id" label="审核员ID" width="140" />
        <el-table-column prop="apply_result" label="申请结果" width="140" >
          <template v-slot ="scope">{{ scope.row.apply_result ? '通过' : '不通过' }}</template>
        </el-table-column>
      <el-table-column prop="apply_result" label="开户状态" width="140" >
          <template v-slot ="scope">{{ scope.row.have_open ? '已开户' : '未开户' }}</template>
        </el-table-column>
        <el-table-column label="具体操作" width="150" >
          <template v-slot="scope">
            <el-button link type="primary"  :disabled="scope.row.have_open || scope.row.apply_result===false"
                       @click="this.newCardVisible=true,
              this.newCardApplyId=scope.row.apply_id,
              this.newCardUserId=scope.row.account_id">开户</el-button>
          </template>
        </el-table-column>
    </el-table>

    <!-- 开户对话框 -->
    <el-dialog v-model="newCardVisible" title="开户" width="30%" align-center>
      确认要开户吗？
      <template #footer>
        <span>
          <el-button @click="this.newCardVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmNewCard">确认</el-button>
        </span>
      </template>
    </el-dialog>

    </el-scrollbar>
</template>

<script>

import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      tableData: [
        {
          apply_id:1,
          apply_date: "",
          apply_result: false,
          account_id: 1, // online_user_id
          credit: '',
          examiner_id: 1,
          have_open: false
        },
      ],
      // 开户
      newCardVisible: false,
      newCardUserId: 1,
      newCardApplyId: 1,
    }
  },
  methods: {
    QueryApplications() {
      axios.get("/creditcard/get_check_applications")
          .then(response => {
            this.tableData = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let application = {
                apply_id: item.apply_id,
                apply_date: item.apply_date,
                apply_result: item.apply_result,
                account_id: item.online_user_id,
                credit: item.credit,
                // 还没有从后端获取 assert：申请人的信誉情况，需要贷款模块提供
                examiner_id: item.examiner_id,
                have_open: item.have_open,
              };
              this.tableData.push(application);
            });
          })
    },
    ConfirmNewCard() {
      console.log(this.newCardApplyId)
      axios.post("/creditcard/add_new_card",
      {
        online_user_id: this.newCardUserId,
        apply_id: this.newCardApplyId,
      })
          .then(response => {
            if(response.data.status === "success") {
              ElMessage.success("开户成功")
              this.newCardVisible = false
              this.QueryApplications()
            } else {
              ElMessage.error("开户失败")
            }
          })
          .catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("开户失败" + error);
          });
    },
  },
  mounted() {
    this.QueryApplications()
  }
}
</script>

<style scoped>
</style>