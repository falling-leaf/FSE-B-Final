<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">

    <!--信用卡审核员信息显示卡片-->
    <div style="margin-left:20px; display: flex;flex-wrap: wrap; justify-content: start;">
      <!-- 添加信用卡审查员 -->
      <el-button class="newExaminerBox" @click="newExaminerVisible = true">
        <el-icon style="height: 50px; width: 50px;">
          <Plus style="height: 100%; width: 100%;" />
        </el-icon>
      </el-button>

      <!-- 数据库中审查员列表卡片 -->
      <div class="examinerBox" v-for="examiner in examiners" :key="examiner.examiner_id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">No. {{examiner.examiner_id}}</div>

          <el-divider />

          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2px;"><span style="font-weight: bold">账户名：</span>{{examiner.account}}</p>
            <p style="padding: 2px;"><span style="font-weight: bold">员工ID：</span>{{examiner.employee_id}}</p>
            <p style="padding: 2px;"><span style="font-weight: bold">姓名：</span>{{ examiner.employee_name }}</p>
            <p style="padding: 2px;"><span style="font-weight: bold">性别：</span>{{ examiner.sex }}</p>
            <p style="padding: 2px;"><span style="font-weight: bold">电话：</span>{{ examiner.phone_number }}</p>
            <p style="padding: 2px;">
              <el-tag v-if="examiner.check_authority">审查权限</el-tag>
            </p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-top: 10px; display:flex; margin-left: 50px; margin-right: 50px;">
            <el-button type="primary" :icon="Edit" @click="this.modifyInfo.examiner_id=examiner.examiner_id,
            this.modifyInfo.new_employee_name=examiner.employee_name, this.modifyInfo.new_account=examiner.account,
              this.modifyExaminerVisible = true"  />
            <el-button type="primary" :icon="Switch" @click="this.toChangeAuthority=examiner.examiner_id,
              this.changeAuthorityVisible = true"  />
            <el-button type="danger" :icon="Delete" @click="this.deleteExaminerId=examiner.examiner_id,
              this.deleteExaminerVisible = true"  />
          </div>

        </div>
      </div>
    </div>

    <!-- 添加审查员对话框 -->
    <el-dialog v-model="newExaminerVisible" title="添加信用卡审查员" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          姓名：
          <el-input v-model="newExaminer.employee_name" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          账号：
          <el-input v-model="newExaminer.account" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          身份证：
          <el-input v-model="newExaminer.identity_card" style="width: 15vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          密码：
          <el-input v-model="newExaminer.password" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          电话：
          <el-input v-model="newExaminer.phone_number" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          性别：
          <el-select v-model="this.newExaminer.sex" style="width: 12.5vw;">
          <el-option v-for="type in sex_types" :key="type.value" :label="type.label" :value="type.value"/>
        </el-select>
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          其他信息：
          <el-input v-model="newExaminer.other_information" style="width: 15vw;" clearable />
      </div>
      <template #footer>
        <span>
          <el-button @click="newExaminerVisible=false">取消</el-button>
          <el-button type="primary" @click="ConfirmNewExaminer"
                     :disabled="newExaminer.employee_name.length===0||newExaminer.sex ===null||
                     newExaminer.account.length===0 || newExaminer.password.length===0||
                     newExaminer.identity_card.length!==18">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除审查员对话框 -->
    <el-dialog v-model="deleteExaminerVisible" title="删除信用卡审查员" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
         <span>确定删除<span style="font-weight: bold;">{{ this.deleteExaminerId }}号信用卡审查员</span>吗？</span>
      </div>

      <template #footer>
        <span>
          <el-button @click="deleteExaminerVisible=false">取消</el-button>
          <el-button type="danger" @click="ConfirmDeleteExaminer">删除</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改审查员对话框 -->
    <el-dialog v-model="modifyExaminerVisible" title="修改信用卡审查员信息" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          账号：
          <el-input v-model="modifyInfo.new_account" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          密码：
          <el-input v-model="modifyInfo.new_password" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          身份证：
          <el-input v-model="modifyInfo.new_identity_card" style="width: 15vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          手机号码：
          <el-input v-model="modifyInfo.new_phone_number" style="width: 12.5vw;" clearable />
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          性别：
          <el-select v-model="this.newExaminer.sex" style="width: 12.5vw;">
          <el-option v-for="type in sex_types" :key="type.value" :label="type.label" :value="type.value"/>
        </el-select>
      </div>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          其他信息：
          <el-input v-model="modifyInfo.new_other_information" style="width: 15vw;" clearable />
      </div>

      <template #footer>
        <span>
          <el-button @click="modifyExaminerVisible=false">取消</el-button>
          <el-button type="primary" @click="ConfirmModifyExaminer"
                     :disabled=" modifyInfo.new_account==='' ||
                     modifyInfo.new_password==='' || modifyInfo.new_employee_name.length===0 ||
                     modifyInfo.new_identity_card.length===0 && modifyInfo.new_phone_number.length===0 ||
                     modifyInfo.new_other_information.length===0">确定</el-button>
        </span>
      </template>
    </el-dialog>

     <!-- 改变权限审查员对话框 -->
    <el-dialog v-model="changeAuthorityVisible" title="改变审查员权限" width="30%" align-center>
      <div style="margin-left: 2vw;   font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          权限操作：
          <el-select v-model="authority_type" style="width: 12.5vw;">
              <el-option v-for="type in authority_types" :key="type.value" :label="type.label" :value="type.value" />
          </el-select>
      </div>
      <template #footer>
        <span>
          <el-button @click="changeAuthorityVisible=false">取消</el-button>
          <el-button type="primary" @click="ConfirmGrant" :disabled="authority_type==='收回权限'">确认授予</el-button>
          <el-button type="primary" @click="ConfirmRevoke" :disabled="authority_type==='授予权限'">确认收回</el-button>
        </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>
<script>


import {Delete, Edit, Plus, Switch} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default{
  data(){
    return{
      examiners: [
        {
          examiner_id: 1,
          account: '', // default: employee_identity_card
          check_authority: '',
          employee_id: '',
          employee_name: '',
          sex:'',
          phone_number:''
        },
      ],
      Delete,
      Edit,
      Plus,
      Switch,
      // add examiner(should by employee_id first)
      newExaminerVisible: false,
      newExaminer:{
        employee_name: '',
        account:'',
        phone_number:'',
        identity_card:'',
        password:'',
        other_information:'',
        sex:'',
      },
      // modify examiner
      modifyExaminerVisible: false,
      modifyInfo: {
        examiner_id: 1,
        new_employee_name:'',
        new_account: '',
        new_password: '',
        new_phone_number:'',
        new_identity_card:'',
        new_other_information:'',
        new_sex:'',
      },
      // delete examiner
      deleteExaminerVisible: false,
      deleteExaminerId: 1,
      // grant or revoke
      changeAuthorityVisible: false,
      authority_types: [
        {
          value: '授予权限',
          label: '授予权限',
        },
        {
          value: '收回权限',
          label: '收回权限',
        },
      ],
      authority_type: '',
      toChangeAuthority: 0,
      sex_types:[{value:'male',label:'男'},{value:'female',label:'女'}],
    }
  },
  methods: {
    ConfirmNewExaminer() {
      //发出POST请求
      axios.post( "/creditcard/add_examiner",
      {
        employee_name: this.newExaminer.employee_name,
        account: this.newExaminer.account,
        phone_number: this.newExaminer.phone_number,
        identity_card: this.newExaminer.identity_card,
        password: this.newExaminer.password,
        other_information: this.newExaminer.other_information,
        sex:this.newExaminer.sex,
      }).then(response => {
            if(response.data.status === 'success') {
              ElMessage.success("添加成功");
              this.newExaminerVisible = false;
              this.QueryExaminers();
            }else{
              ElMessage.error("添加失败："+ response.data.message);
            }
      }).catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("添加失败" + error);
          });
    },
    ConfirmModifyExaminer() {
      //发出
      axios.post( "/creditcard/modify_examiner",
      {
        examiner_id: this.modifyInfo.examiner_id,
        new_account: this.modifyInfo.new_account,
        new_password: this.modifyInfo.new_password,
        new_employee_name: this.modifyInfo.new_employee_name,
        new_phone_number: this.modifyInfo.new_phone_number,
        new_identity_card: this.modifyInfo.new_identity_card,
        new_other_information: this.modifyInfo.new_other_information,
        new_sex:this.modifyInfo.new_sex,
      }).then(response => {
            if(response.data.status === 'success'){
              ElMessage.success("修改成功");
              this.modifyExaminerVisible = false;
              this.QueryExaminers();
            }else{
              ElMessage.error("修改失败："+ response.data.message);
            }
          })
          .catch(error => {
            console.error('Error modifying examiners:', error);
            ElMessage.error("修改失败：" + error);
          });
    },
    ConfirmDeleteExaminer() {
      //发出POST请求
      axios.post( "/creditcard/delete_examiner", {
        examiner_id: this.deleteExaminerId,
      })
          .then(response => {
           if(response.data.status === 'success'){
             ElMessage.success("删除成功");
              this.QueryExaminers();
              this.deleteExaminerVisible = false;
           }else{
             ElMessage.error("删除失败："+ response.data.message);
           }
          })
          .catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("删除失败：" + error);
          });
    },
    ConfirmGrant() {
      //发出POST请求
      axios.post( "/creditcard/grant_authority", {
        examiner_id: this.toChangeAuthority,
      })
          .then(response => {
            // let status =  response.data.status
            if(response.data.status === 'success'){
              ElMessage.success("权限变更成功");
              this.changeAuthorityVisible = false;
              this.QueryExaminers();
            }else {
              ElMessage.error("权限变更失败："+ response.data.message);
            }
          })
          .catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("权限变更失败：" + error);
          });
    },
    ConfirmRevoke() {
      //发出POST请求
      axios.post( "/creditcard/revoke_authority", {
        examiner_id: this.toChangeAuthority,
      })
          .then(response => {
            if(response.data.status === 'success'){
              ElMessage.success("权限变更成功");
              this.changeAuthorityVisible = false;
              this.QueryExaminers();
            }else{
              ElMessage.error("权限变更失败："+ response.data.message);
            }
          })
          .catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("权限变更失败：" + error);
          });
    },
    QueryExaminers() {
      axios.get("/creditcard/get_examiners")
          .then(response => {
            this.examiners = [];
            let examiners = response.data.list;
            examiners.forEach(item => {
              let examiner = {
                examiner_id: item.examiner_id,
                account: item.account,
                check_authority: item.check_authority,
                employee_name: item.employee_name, // 这里假设没有从后端获取 employee_name
                sex: item.sex,
                phone_number: item.phone_number,
                employee_id:item.employee_id,
              };
              this.examiners.push(examiner);
            });
          })
    },

  },
  mounted() { // 当页面被渲染时
    this.QueryExaminers();
  }
}
</script>

<style scoped>
.examinerBox {
  height:380px;
  width: 275px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 28px;
  margin-right: 10px;
  padding: 15px 10px 8px 8px;
}
.newExaminerBox {
  height: 380px;
  width: 275px;
  margin-top: 40px;
  margin-left: 28px;
  margin-right: 10px;
  padding: 15px 10px 8px 8px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}
</style>