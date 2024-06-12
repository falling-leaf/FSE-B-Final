<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%; ">
        <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">
            交易历史
            <el-tooltip content="搜索交易历史" placement="top">
                <el-button type="primary" :icon="Search" @click="isDisplaySearchBox = true" circle></el-button>
            </el-tooltip>
        </div>

        <el-dialog v-model="isDisplaySearchBox" :title="'搜索条件'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                外币:
                <el-select v-model="this.currencyNameCondition" placeholder="请选择外币" style="width: 12.5vw;">
                    <el-option v-for="option in currencyOptions" :key="option.value" :label="option.label" :value="option.value"></el-option>
                </el-select>
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                银行卡号:
                <el-select v-model="this.accountIdCondition" placeholder="请选择银行卡号" style="width: 12.5vw;">
                    <el-option v-for="option in accountIdOptions" :key="option.value" :label="option.label" :value="option.value"></el-option>
                </el-select>
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                银行卡号:
                <el-select v-model="this.tradingStateCondition" placeholder="请选择银行卡号" style="width: 12.5vw;">
                    <el-option label="买入" value="买入"></el-option>
                    <el-option label="卖出" value="卖出"></el-option>
                </el-select>
            </div>
            <!-- TODO: 选择交易状态的栏 -->
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                日期:
                <a-date-picker
                    :picker="pickerType"
                    :format="dateFormat"
                    :value="startDate"
                    @change="handleStartDateChange"
                    style="margin-right: 10px; "
                ></a-date-picker>
                <span style="margin-right: 10px;">-</span>
                <a-date-picker
                    :picker="pickerType"
                    :format="dateFormat"
                    :value="endDate"
                    @change="handleEndDateChange"
                    style="margin-right: 20px; "
                ></a-date-picker>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="getHistory()">搜索</el-button>
                    <el-button @click="isDisplaySearchBox = false">取消</el-button>
                </span>
            </template>
        </el-dialog>
    
        <el-table ref="dataTable" v-if="isShow" :data="this.tableData" height="555" :table-layout="'auto'"
                style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
            <el-table-column prop="account_id" label="交易银行卡" sortable></el-table-column>
            <el-table-column prop="currency_name" label="外币" sortable></el-table-column>
            <el-table-column prop="trading_state" label="交易状态" sortable></el-table-column>
            <el-table-column prop="rmb_amount" label="人民币交易额" sortable></el-table-column>
            <el-table-column prop="currency_amount" label="外币交易额" sortable></el-table-column>
            <el-table-column prop="trading_datetime" label="交易时间" sortable></el-table-column>
        </el-table>
    </el-scrollbar>
</template>
  
<script>
  
import { Delete, Edit, Search, Plus, ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, datePickerProps, ElButton } from 'element-plus'
import axios from 'axios'
import { DatePicker } from 'ant-design-vue'
import dayjs from 'dayjs'
import { Chart } from 'chart.js/auto'
  
export default {
    components: {
        ADatePicker: DatePicker,
    },
    data () {
        return {
            tableData: [{
                account_id: 0,
                currency_id: 0,
                currency_name: '',
                trading_state: '',
                rmb_amount: 0,
                currency_amount: 0,
                trading_datetime: '',
            }],
            userId: 1,
            pickerType: 'date',
            dateFormat: 'YYYY-MM-DD',
            Delete,
            Edit,
            Search,
            Plus,
            ArrowLeft,
            isShow: true,
            tradingStateCondition: '',
            maxTradingDatetimeCondition: '',
            minTradingDatetimeCondition: '',
            currencyNameCondition: '',
            accountIdCondition: 0,
            accountIdOptions: [{
                label: '',
                value: '',
            }],
            currencyOptions: [{
                label: '',
                value: '',
            }],
            isDisplaySearchBox: false,
            startDate: null,
            endDate: null,
        }
    },
    methods: {
        handleStartDateChange(date, dateString) {
            this.startDate = date;
            this.minTradingDatetimeCondition = dateString;
            //console.log("Received date:", date);
            //console.log("Received date string:", dateString);
        },
        handleEndDateChange(date, dateString) {
            this.endDate = date;
            this.maxTradingDatetimeCondition = dateString;
            //console.log("Received date:", date);
            //console.log("Received date string:", dateString);
        },
        myTimeToLocal(inputTime){
            let res = inputTime.replace('T', ' ');
            res = res.replace('Z', '')
            return res;
        },
        async getAllAccountId() {
            this.accountIdOptions = []

            /*await axios.get('url to get all accountId')
                .then(response => {
                    //console.log(response.data)
                    if(response.data.error_num === 0) {
                        let datas = response.data.data
                        datas.forEach(element => {
                            this.options.push(element)
                        })
                    } else {
                        ElMessage.error("银行卡号列表请求错误")
                        //console.log(response.data.msg)
                    }
                })*/
        },
        async getAllCurrency() {
            this.currencyOptions = []

            await axios.get('/FExchange/user/currency/category')
                .then(response => {
                    //console.log(response.data)
                    if(response.data.error_num === 0) {
                        let datas = response.data.data
                        datas.forEach(element => {
                            this.currencyOptions.push(element)
                        })
                    } else {
                        ElMessage.error("外币列表请求错误")
                        //console.log(response.data.msg)
                    }
                })
        },
        async getHistory() {
        this.tableData = []

        let queryParams = {}
        if(this.maxTradingDatetimeCondition != '') {
            queryParams.maxDatetime = this.maxTradingDatetimeCondition
        }
        if(this.minTradingDatetimeCondition != '') {
            queryParams.minDatetime = this.minTradingDatetimeCondition
        }
        if(this.tradingStateCondition != '') {
            queryParams.tradingState = this.tradingStateCondition
        }
        if(this.currencyNameCondition != '') {
            queryParams.currencyName = this.currencyNameCondition
        }
        if(this.accountIdCondition != 0) {
            queryParams.accountId = this.accountIdCondition
        }
        if(this.userId != 0) {
            queryParams.userId = this.userId
        }
        
        await axios.get('/FExchange/user/history/get', { params: queryParams })
            .then(response => {
                //console.log(queryParams)
                //console.log(response.data)
                if(response.data.error_num === 0) {
                    let datas = response.data.histories
                    datas.forEach(element => {
                    element.rmb_amount = parseFloat(element.rmb_amount).toFixed(2)
                    element.currency_amount = parseFloat(element.currency_amount).toFixed(2)
                    element.trading_datetime = this.myTimeToLocal(element.trading_datetime)
                    this.tableData.push(element)
                    this.isDisplaySearchBox = false
                    })
                } else {
                    ElMessage.error("交易历史数据请求错误")
                    //console.log(response.data.msg)
                }
            })
        }
    },
    mounted() {
        this.getHistory()
        this.getAllCurrency()
        this.getAllAccountId()
    }
}
</script>