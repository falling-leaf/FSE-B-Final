<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        未审核的信用卡申请单
    </div>

    <!-- 记录 -->
    <el-table :data="tableData" height="600" stripe
        :default-sort="{ prop: 'apply_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
        <el-table-column prop="apply_id" label="申请序号" sortable width="150"/>
        <el-table-column prop="apply_date" label="申请时间" width="220"/>
        <el-table-column prop="account_id" label="申请人ID" />
        <el-table-column prop="credit" label="申请人信誉" />

        <el-table-column fixed="right" label="具体操作">
          <template v-slot="scope">
            <el-button link type="primary"  @click="this.checkInfo.apply_id = scope.row.apply_id,
              this.checkAssetVisible = true;">审核</el-button>
          </template>

        </el-table-column>
    </el-table>

    <!-- 审核对话框 -->
    <el-dialog v-model="checkAssetVisible" title="审核" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          申请结果：
        <el-select v-model="this.checkInfo.apply_result" style="width: 12.5vw;">
          <el-option v-for="type in result_types" :key="type.value" :label="type.label" :value="type.value"/>
        </el-select>
      </div>

      <template #footer>
        <span>
          <el-button @click="this.checkAssetVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmChangeState">确认</el-button>
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
      examiner_id: 2,
      tableData: [
        {
          apply_id:'',
          account_id: '', // online_user
          apply_date: "",
          credit: "",
        },
      ],
      // 审核
      checkAssetVisible : false,
      checkInfo: {
        examiner_id: '',
        apply_id: '',
        apply_result: '',
      },
       result_types: [
          { value: true, label: '通过',},
        { value: false, label: '不通过',}
      ]
    }
  },
  methods: {
    QueryApplications() {
      axios.get("/creditcard/get_uncheck_applications")
          .then(response => {
            this.tableData = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let application = {
                apply_id: item.apply_id,
                apply_date: item.apply_date,
                account_id: item.online_user_id,
                credit: item.credit,
              };
              this.tableData.push(application);
            });
          })
    },
    ConfirmChangeState() {
      axios.post("/creditcard/change_application_state",
      {
        apply_id: this.checkInfo.apply_id,
        examiner_id: this.examiner_id,
        apply_result: this.checkInfo.apply_result,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("修改成功");
              this.checkAssetVisible = false;
              this.QueryApplications();
            } else {
              ElMessage.error("修改失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("修改失败" + error);
          });
    },

  },
  mounted() {
    this.QueryApplications()
  },
}
</script>

<style scoped>
</style>