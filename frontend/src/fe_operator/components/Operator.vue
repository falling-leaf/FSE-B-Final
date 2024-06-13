<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%; ">

        <el-dialog v-model="isConfirmDeleteCurrency" :title="'删除确认'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 10px; ">
                是否确认删除外币： {{ this.detailTitle }}
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 30px; ">
                提示：删除后与该外币有关的所有信息都将被删除
            </div>
            
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleDeleteCurrency()">确认删除</el-button>
                    <el-button @click="isConfirmDeleteCurrency = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isModifyNameCurrency" :title="'重命名'" width="35%"
            align-center>
            <h1 class="h11">输入新名称：<input type="text" id="modify_name" v-model="modify_name" class="input" required></h1>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleModifyNameCurrency()">确认修改</el-button>
                    <el-button @click="isModifyNameCurrency = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="isModifyRateCurrency" :title="'更新汇率'" width="35%"
            align-center>
            <h1 class="h11">预期买入价：<input type="text" id="modify_latest_buy" v-model="modify_latest_buy" class="input" required></h1>
            <h1 class="h11">预期卖出价：<input type="text" id="modify_latest_sell" v-model="modify_latest_sell" class="input" required></h1>
            
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleModifyRateCurrency()">确认更新</el-button>
                    <el-button @click="isModifyRateCurrency = false">取消</el-button>
                </span>
            </template>
        </el-dialog>


        <div v-if="isShow" style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">外币列表    
            <input type="text" id="searchtext" v-model="searchtext" class="input">
            <el-tooltip content="搜索外币" placement="top">
                <el-button type="primary" :icon="Search" @click="handlesearch(1)" circle></el-button>
            </el-tooltip>
            <div>
                <button v-if='issearch' @click="issearch = false, searchRecords(1)">返回</button>
            </div>
        </div>


        <el-table ref="dataTable" v-if="isShow" :data="fitlerTableData" height="555" :table-layout="'auto'"
            style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
            <el-table-column prop="currency_name" label="外币" sortable></el-table-column>
            <el-table-column prop="buying_rate" label="现汇买入价" sortable></el-table-column>
            <el-table-column prop="selling_rate" label="现汇卖出价" sortable></el-table-column>
            <el-table-column prop="update_datetime" label="更新时间" sortable></el-table-column>
            <el-table-column label="操作">
                <template v-slot="{ row }">
                    <el-button @click="deletes(row)" type="text">删除</el-button>
                    <el-button @click="modifys(row)" type="text">更新</el-button>
                    <el-button @click="rename(row)" type="text">重命名</el-button>
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
            foreign_exchange_operator_id: 1,
            isShow: true, // 结果表格展示状态
            isDisplaySearchBox: false, // 搜索界面显示
            issearch: false,
            isShowDetails: false,
            isConfirmDeleteCurrency: false,
            isModifyRateCurrency: false,
            isModifyNameCurrency: false,
            detailTitle: '',
            curPage: 1,
            Edit,
            Delete,
            Search,
            Plus,
            ArrowLeft,
            pickerType: 'date',
            dateFormat: 'YYYY-MM-DD',
            delete_currency_name: '',
            searchtext:'',
            modify_name: '',
            modify_latest_buy: '',
            modify_latest_sell: '',
            selectedRowData: null,
            chart: null,
            tableData: [{
                currency_id: 0,
                currency_name: '',
                buying_rate: '',
                selling_rate: '',
                update_datetime: '',
            }],
        }
    },
    created() {
        this.fetchDataFromUrl();
    },
    computed: {
        fitlerTableData() {
            return this.tableData;
        }
    },
    methods: {
        fetchDataFromUrl() {
            // 获取当前URL
            const url = new URL(window.location);
            // 创建URLSearchParams对象
            const params = new URLSearchParams(url.search);
            // 从查询字符串中获取参数
            this.foreign_exchange_operator_id = params.get('foreign_exchange_operator_id');
        },
        handlePrevPage() {
            if(this.curPage > 1) {
                this.curPage--
                if(this.issearch==true){
                    this.handlesearch(this.curPage)
                }
                else
                {
                    this.searchRecords(this.curPage)
                }
            } else {
                ElMessage.warning("没有上一页了")
            }
        },
        async handleNextPage() {
            this.curPage++
            if(this.issearch==true){
                await this.handlesearch(this.curPage)
            }
            else
            {
                await this.searchRecords(this.curPage)
            }
            if(this.tableData.length === 0) {
                ElMessage.warning("没有下一页了")
                this.handlePrevPage()
            }
        },
        async handlesearch(page){
            let queryParams = {}
            if(page != -1) {
                queryParams.curPage = page
                this.curPage = page
            }
            if(this.searchtext != '') {
                this.issearch = true
                this.tableData = []
                queryParams.name = this.searchtext
                await axios.get('/FExchange/Operator/search', { params: queryParams })
                    .then(response => {
                        this.tableData = response.data.results;
                    })
                .catch(error => {
                    ElMessage.warning('Error fetching data:', error);
                });
            }
            else
            {
                
            }
        },
        async handleModifyNameCurrency(){
            this.isModifyNameCurrency = false
            let renameParams = {}
            if(this.mofidy_name != '') {
                renameParams.currency_name = this.modify_name
            }
            renameParams.currency_id = this.selectedRowData.currency_id
            renameParams.operator_id = this.foreign_exchange_operator_id
            await axios.post('/FExchange/Operator/rename', renameParams)
            .then(response => {
                console.log(response.data);
                if (response.data.status === 'success') {
                    ElMessage.warning('Currency rename successfully')
                } else {
                    ElMessage.error(response.data.message)
                }
            })
            .catch(error => {
                ElMessage.warning('重命名请求发送失败', error);
            });
        },
        async handleDeleteCurrency(){
            this.isConfirmDeleteCurrency = false
            let deleteParams = {}
            deleteParams.currency_id = this.selectedRowData.currency_id
            deleteParams.operator_id = this.foreign_exchange_operator_id
            await axios.post('/FExchange/Operator/delete',deleteParams)
            .then(response => {
                console.log(response.data);
                if (response.data.status === 'success') {
                    ElMessage.warning('Currency deleted successfully');
                } else {
                    ElMessage.error(response.data.message)
                }
            })
            .catch(error => {
                ElMessage.warning('删除请求发送失败', error);
            });
        },
        async handleModifyRateCurrency(){
            this.isModifyRateCurrency = false
            let modifyParams = {}
            if(this.mofidy_latest_buy != '') {
                modifyParams.buying_rate = this.modify_latest_buy
            }
            if(this.modify_latest_sell != '') {
                modifyParams.selling_rate = this.modify_latest_sell
            }
            modifyParams.currency_id = this.selectedRowData.currency_id
            modifyParams.operator_id = this.foreign_exchange_operator_id
            await axios.post('/FExchange/Operator/modify', modifyParams)
            .then(response => {
                console.log(response.data);
                if (response.data.status === 'success') {
                    ElMessage.warning('Currency modify successfully')
                } else {
                    ElMessage.error(response.data.message)
                }
            })
            .catch(error => {
                ElMessage.warning('添加请求发送失败', error);
            });
        },
        async deletes(row) {
            this.selectedRowData = row
            this.isConfirmDeleteCurrency = true
            this.detailTitle = this.selectedRowData.currency_name
        },
        async modifys(row) {
            this.selectedRowData = row
            this.isModifyRateCurrency = true
        },
        async rename(row) {
            this.selectedRowData = row
            this.isModifyNameCurrency = true
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
                queryParams.curPage = page
                this.curPage = page
            }
            await axios.get('/FExchange/Operator/show', { params: queryParams })
                .then(response => {
                    if(response.data.error_num === 0) {
                        console.log(response.data)
                        let records = response.data.record
                        let names = response.data.name
                        records.forEach(element => {
                            this.tableData.push(element.fields)
                        })
                        let i = 0
                        names.forEach(element => {
                            this.tableData[i].currency_name = element.fields.currency_name
                            this.tableData[i].update_datetime = this.myTimeToLocal(this.tableData[i].update_datetime)
                            i++
                        })
                        this.isDisplaySearchBox = false
                    } else {
                        ElMessage.error("搜索请求错误")
                        console.log(response.data)
                    }
                })
        },
        async getAllCurrency() {
            this.options = []

            await axios.get('/FExchange/user/currency/category')
                .then(response => {
                    //console.log(response.data)
                    if(response.data.error_num === 0) {
                        let datas = response.data.data
                        datas.forEach(element => {
                            this.options.push(element)
                        })
                    } else {
                        ElMessage.error("外币列表请求错误")
                        //console.log(response.data.msg)
                    }
                })
        },
    },
    mounted() {
        this.searchRecords(1)
        this.getAllCurrency()
    }
}
</script>

<style>
  .h11{
    margin-left: 5px;
    color: #222222;
    font-size: medium;
    margin-top:30px;
    margin-bottom: 30px;
  }
  .input{
    margin-left: 20px;
    margin-bottom: 20px;
    font-size:medium;
    width:200px;
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