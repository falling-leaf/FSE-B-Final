<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%; ">

        <el-dialog v-model="isAddOperator" :title="'新增操作员账号'" width="35%" align-center>
            <div>
                <h1 class="h11">姓名：<input type="text" id="employee_name" v-model="employee_name" class="inputtext" required></h1>
                <h1 class="h11">账号：<input type="text" id="account" v-model="account" class="inputtext" required></h1>
                <h1 class="h11">身份证号：<input type="text" id="identity_card" v-model="identity_card" class="inputtext" required></h1>
                <h1 class="h11">性别：
                        <input type="radio" v-model="selectedOption" value="male"> 男
                        <input type="radio" v-model="selectedOption" value="female"> 女
                </h1>
                <h1 class="h11">电话号码：<input type="text" id="phone_number" v-model="phone_number" class="inputtext" required></h1>
                <h1 class="h11">密码：<input type="password" id="password" v-model="password" class="inputtext" required></h1>
                <h1 class="h11">确认密码：<input type="password" id="confirm_password" v-model="confirm_password" class="inputtext" required></h1>
                <h1 class="h11">职位：外汇操作员</h1>
                <h1 class="h11">是否在任：是</h1>
                <h1 class="h11">其他信息：<input type="text" id="other_information" v-model="other_information" class="inputtext" required></h1>
                <h1 class="h11">权限设置：</h1>
                <h1 style="margin-left: 70px; color: #222222; font-size: medium; margin-bottom: 20px;">
                    <div v-for="checkbox in checkboxes" :key="checkbox.value">
                    <input type="checkbox" :value="checkbox.value" v-model="checkedValues" style="margin-bottom: 20px; font-size: medium; width:30px; margin-right: 20px;"> {{ checkbox.label }}
                    </div>
                </h1>
            </div>
            <template #footer>
                <span class="dialog-footer">
                <el-button @click="handleAddOperator">确认添加</el-button>
                <el-button @click="isAddOperator = false">取消</el-button>
                </span>
            </template>
        </el-dialog>
        
        <el-dialog v-model="isModifyOperator" :title="'修改权限'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 10px; ">
                <div v-for="checkbox in checkboxes" :key="checkbox.value">
                <input type="checkbox" :value="checkbox.value" v-model="checkedValues"> {{ checkbox.label }}
                </div>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleModifyOperator()">确认修改</el-button>
                    <el-button @click="isModifyOperator = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isModifyOperator" :title="'修改权限'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 10px; ">
                <div v-for="checkbox in checkboxes" :key="checkbox.value">
                <input type="checkbox" :value="checkbox.value" v-model="checkedValues"> {{ checkbox.label }}
                </div>
            </div>
            
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleModifyOperator()">确认修改</el-button>
                    <el-button @click="isModifyOperator = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isConfirmDeleteOperator" :title="'删除确认'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 10px; ">
                是否确认删除操作员账户： {{ this.detailTitle }}
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 30px; ">
                提示：删除后与该账户有关的所有信息都将被删除
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleDeleteOperator()">确认删除</el-button>
                    <el-button @click="isConfirmDeleteOperator = false">取消</el-button>
                </span>
            </template>
        </el-dialog>


        <div v-if="isShow" style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">外汇操作员列表    
            
            <input type="text" id="searchOperator" v-model="searchOperator" class="input">
            <el-tooltip content="搜索账号" placement="top">
                <el-button type="primary" :icon="Search" @click="handlesearch(1)" circle></el-button>
            </el-tooltip>
            <button @click="isAddOperator = true" style =" margin-left: 150px;">+</button>
            <div>
                <button v-if='issearch' @click="issearch = false, searchRecords(1)">返回</button>
            </div>
        </div>


        <el-table ref="dataTable" v-if="isShow" :data="fitlerTableData" height="555" :table-layout="'auto'"
            style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
            <el-table-column prop="employee_name" label="操作员姓名" sortable></el-table-column>
            <el-table-column prop="account" label="账号" sortable></el-table-column>
            <el-table-column prop="add_authority" label="新增外币权限" sortable></el-table-column>
            <el-table-column prop="delete_authority" label="删除外币权限" sortable></el-table-column>
            <el-table-column prop="alter_name_authority" label="重命名外币权限" sortable></el-table-column>
            <el-table-column prop="alter_rate_authority" label="更新外币汇率权限" sortable></el-table-column>
            <el-table-column label="操作">
                <template v-slot="{ row }">
                    <el-button @click="deletes(row)" type="text">删除</el-button>
                    <el-button @click="modifys(row)" type="text">更新权限</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!-- 分页按钮 -->
        <div style="text-align: center; margin-top: 20px;">
            <el-button v-if="isShow" @click="handlePrevPage">上一页</el-button>
            <el-button v-if="isShow" @click="handleNextPage">下一页</el-button>
        </div>
    </el-scrollbar>
</template>

<script>
import { Delete, Edit, Search, Plus, ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, datePickerProps, ElButton } from 'element-plus'
import axios from 'axios'
import { DatePicker } from 'ant-design-vue'


export default {
    components: {
        ADatePicker: DatePicker,
    },
    data () {
        return {
            isShow: true, // 结果表格展示状态
            isDisplaySearchBox: false, // 搜索界面显示
            isAddOperator: false,
            ischecked: false,
            selectedRowData: null,
            issearch: false,
            isShowDetails: false,
            isConfirmDeleteOperator: false,
            isModifyOperator: false,
            nowPage: 1,
            employee_name:'',
            identity_card:'',
            phone_number:'',
            account: '',
            password: '',
            confirm_password: '',
            other_information: '',
            searchOperator: '',
            
            selectedOption: '',
            Edit,
            Delete,
            Search,
            Plus,
            ArrowLeft,
            pickerType: 'date',
            dateFormat: 'YYYY-MM-DD',
            delete_currency_name: '',
            tableData: [{
                employee_id: 0,
                foreign_exchange_operator_id: 0,
                employee_name: '',
                account:'',
                add_authority: '', 
                delete_authority: '',
                alter_name_authority: '', 
                alter_rate_authority: ''
            }],
            detailTitle: '',
            checkboxes: [
                { label: '新增外币权限', value: '1' },
                { label: '删除外币权限', value: '2' },
                { label: '重命名权限', value: '4' },
                { label: '修改外币汇率权限', value: '3' }
            ],
            checkedValues: []
        }
    },
    computed: {
        fitlerTableData() {
                return this.tableData;
        }
    },
    mounted() {
        this.searchRecords(1)
    },
    methods: {
        handleStartDateChange(date, dateString) {
            this.startDate = date;
            this.minDateCondition = dateString;
        },
        handleEndDateChange(date, dateString) {
            this.endDate = date;
            this.maxDateCondition = dateString;
        },
        handlePrevPage() {
            if(this.nowPage > 1) {
                this.nowPage--
                if(this.issearch == false)
                {
                    this.searchRecords(this.nowPage)
                }
                else
                {
                    this.handlesearch(this.nowPage)
                }
            } else {
                ElMessage.warning("没有上一页了")
            }
        },
        async handleNextPage() {
            this.nowPage++
            if(this.issearch == false)
            {
                await this.searchRecords(this.nowPage)
            }
            else
            {
                await this.handlesearch(this.nowPage)
            }
            if(this.tableData.length === 0) {
                ElMessage.warning("没有下一页了")
                this.handlePrevPage()
            }
        },
        async handleAddOperator() {
            if(this.password == this.confirm_password){
                let addParams = {}
                addParams.employee_name = this.employee_name
                addParams.account = this.account
                addParams.phone_number = this.phone_number
                addParams.identity_card = this.identity_card
                addParams.password = this.password
                addParams.other_information = this.other_information
                addParams.checkedValues = this.checkedValues
                addParams.selectedOption = this.selectedOption
                await axios.post('/FExchange/foreign/add', addParams)
                .then(response => {
                    console.log(response.data);
                    if (response.data.status === 'success') {
                        ElMessage.success('Currency add successfully');
                        this.employee_name = ''
                        this.account = ''
                        this.phone_number = ''
                        this.identity_card = ''
                        this.password = ''
                        this.other_information = ''
                        this.checkedValues = []
                        this.selectedOption = ''
                        this.confirm_password = ''
                    } else {
                        alert('Error: ' + response.data.message);
                    }
                    })
                .catch(error => {
                    ElMessage.warning('添加请求发送失败', error);
                });
            }
            else{
                ElMessage.warning('两次密码不一致！')
                return;
            }
            this.isAddOperator = false
            this.searchRecords(1)
        },
        async handlesearch(page){
            if(this.searchOperator != '') {
                this.issearch = true
                this.tableData = []
                let searchParams = {}
                if(page != -1) {
                    searchParams.nowPage = page
                    this.nowPage= page
                }
                searchParams.name = this.searchOperator
                await axios.get('/FExchange/foreign/search', { params: searchParams })
                .then(response => {
                    let results = response.data.results
                    this.tableData = results.map(result => {
                        return {
                            employee_id:result.employee_id,
                            foreign_exchange_operator_id: result.foreign_exchange_operator_id,
                            employee_name: result.employee_name,
                            account: result.account,
                            add_authority: result.add_authority,
                            delete_authority: result.delete_authority,
                            alter_name_authority: result.alter_name_authority,
                            alter_rate_authority: result.alter_rate_authority
                        };
                    });
                })
                .catch(error => {
                    ElMessage.warning('Error fetching data:', error);
                });
            }
            else
            {
                this.searchRecords(page)
            }
            this.issearch = false
        },
        async handleModifyOperator(){
            let modifyParams = {}
            modifyParams.checkedValues = this.checkedValues
            modifyParams.foreign_exchange_operator_id = this.selectedRowData.foreign_exchange_operator_id
            await axios.post('/FExchange/foreign/updateauthority',modifyParams)
            .then(response => {
                if (response.data.status === 'success') {
                    ElMessage.warning('Operator modify successfully');
                } else {
                    alert('Error: ' + response.data.message);
                }
            })
            .catch(error => {
                ElMessage.warning('权限更新请求发送失败', error);
            });
            this.isModifyOperator = false
            this.searchRecords(1)
        },
        async handleDeleteOperator(){
            let deleteParams = {}
            deleteParams.foreign_exchange_operator_id = this.selectedRowData.foreign_exchange_operator_id
            deleteParams.employee_id = this.selectedRowData.employee_id
            await axios.post('/FExchange/foreign/delete',deleteParams)
            .then(response => {
                if (response.data.status === 'success') {
                    ElMessage.warning('Currency deleted successfully');
                } else {
                alert('Error: ' + response.data.message);
                }
            })
            .catch(error => {
                ElMessage.warning('删除请求发送失败', error);
            });
            this.isConfirmDeleteOperator = false
            this.searchRecords(1)
        },
        async deletes(row) {
            this.selectedRowData = row
            this.isConfirmDeleteOperator = true
            this.detailTitle = this.selectedRowData.employee_name
        },
        async modifys(row) {
            this.selectedRowData = row
            this.isModifyOperator = true
        },
        async details(row) {
            this.selectedRowData = row
        },
        myTimeToLocal(inputTime){
            let res = inputTime.replace('T', ' ');
            res = res.replace('Z', '')
            return res;
        },
        async searchRecords(page) {
            this.tableData = []

            let queryParams = {}
            if(page != -1) {
                queryParams.nowPage = page
                this.nowPage = page
            }
            
            await axios.get('/FExchange/foreign/searchall', { params: queryParams })
                .then(response => {
                    let results = response.data.results
                    this.tableData = results.map(result => {
                        return {
                            employee_id:result.employee_id,
                            foreign_exchange_operator_id: result.foreign_exchange_operator_id,
                            employee_name: result.employee_name,
                            account: result.account,
                            add_authority: result.add_authority,
                            delete_authority: result.delete_authority,
                            alter_name_authority: result.alter_name_authority,
                            alter_rate_authority: result.alter_rate_authority
                        };
                    });
                })
                .catch(error => {
                    ElMessage.warning('Error fetching data',error);
                });
        }
    }
}
</script>

<style>
  .h11{
    margin-left: 50px;
    color: #222222;
    font-size: medium;
    margin-top:20px;
    margin-bottom: 20px;
  }
  label {
    display: block;
    margin-bottom:5px;
  }
  .input{
    margin-left: 525px;
    margin-bottom: 20px;
    font-size:medium;
    width:200px;
    margin-right: 20px;
  }
  .inputtext{
    margin-left: 20px;
    font-size:medium;
    width:230px;
    margin-right: 20px;
  }
  button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}
  </style>