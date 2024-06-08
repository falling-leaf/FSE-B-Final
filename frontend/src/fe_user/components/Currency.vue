<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%; ">

        <div v-if="isShowDetails" style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">
            {{ this.detailTitle }}
            <el-tooltip content="返回上一页面" placement="top">
                <el-button type="primary" :icon="ArrowLeft" @click="this.isShowDetails = false, this.isShow = true" circle ></el-button>
            </el-tooltip>
        </div>

        <div v-if="isShowDetails">
            <canvas ref="lineChart" style="width: 800px; height: 400px;"></canvas>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <el-button v-if="isShowDetails" @click="handleBuyCurrency">购买外币</el-button>
            <el-button v-if="isShowDetails" @click="handleSellCurrency">卖出外币</el-button>
        </div>

        <div v-if="isShow" style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold; ">外币列表    
            <el-tooltip content="搜索外币" placement="top">
                <el-button type="primary" :icon="Search" @click="isDisplaySearchBox = true" circle></el-button>
            </el-tooltip>
        </div>

        <el-dialog v-model="isDisplaySearchBox" :title="'搜索条件'" width="30%"
            align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                外币:
                <el-select v-model="this.categoryCondition" placeholder="请选择外币" style="width: 12.5vw;">
                    <el-option v-for="option in options" :key="option.value" :label="option.label" :value="option.value"></el-option>
                </el-select>
            </div>
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
                    <el-button @click="searchRecords(1)">搜索</el-button>
                    <el-button @click="isDisplaySearchBox = false">取消</el-button>
                </span>
            </template>
        </el-dialog>

        <el-table ref="dataTable" v-if="isShow" :data="fitlerTableData" height="555" :table-layout="'auto'"
            style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
            <el-table-column prop="currency_name" label="外币" sortable></el-table-column>
            <el-table-column prop="buying_rate" label="现汇买入价" sortable></el-table-column>
            <el-table-column prop="selling_rate" label="现汇卖出价" sortable></el-table-column>
            <el-table-column prop="update_datetime" label="更新时间" sortable></el-table-column>
            <el-table-column label="操作">
                <template v-slot="{ row }">
                    <el-button @click="details(row)" type="text">详情</el-button>
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
import dayjs from 'dayjs'
import { Chart } from 'chart.js/auto'

export default {
    components: {
        ADatePicker: DatePicker,
    },
    data () {
        return {
            isShow: true, // 结果表格展示状态
            isDisplaySearchBox: false, // 搜索界面显示
            curPage: 1,
            Edit,
            Delete,
            Search,
            Plus,
            ArrowLeft,
            pickerType: 'date',
            dateFormat: 'YYYY-MM-DD',
            tableData: [{
                currency: 0,
                currency_name: '',
                buying_rate: '',
                selling_rate: '',
                update_datetime: '',
            }],
            chart: null,
            simulationData: [
                { buying_rate: 10.5, selling_rate: 15.2, update_datetime: '2024-06-01 08:30:00' },
                { buying_rate: 12.3, selling_rate: 17.1, update_datetime: '2024-06-02 09:45:00' },
                { buying_rate: 8.7, selling_rate: 13.8, update_datetime: '2024-06-03 10:15:00' }
            ],
            selectedRowData: null,
            isShowDetails: false,
            startDate: null,
            endDate: null,
            minDateCondition: '',
            maxDateCondition: '',
            categoryCondition: '',
            options: [{
                label: '',
                value: '',
            }],
            detailTitle: '',
        }
    },
    computed: {
        fitlerTableData() {
            return this.tableData;
        }
    },
    methods: {
        handleBuyCurrency() {
            this.$router.push('/FExchange/user/buy')
        },
        handleSellCurrency() {
            this.$router.push('/FExchange/user/sell')
        },
        handleStartDateChange(date, dateString) {
            this.startDate = date;
            this.minDateCondition = dateString;
            //console.log("Received date:", date);
            //console.log("Received date string:", dateString);
        },
        handleEndDateChange(date, dateString) {
            this.endDate = date;
            this.maxDateCondition = dateString;
            //console.log("Received date:", date);
            //console.log("Received date string:", dateString);
        },
        handlePrevPage() {
            if(this.curPage > 1) {
                this.curPage--
                this.searchRecords(this.curPage)
            } else {
                ElMessage.warning("没有上一页了")
            }
        },
        async handleNextPage() {
            this.curPage++
            await this.searchRecords(this.curPage)
            if(this.tableData.length === 0) {
                ElMessage.warning("没有下一页了")
                this.handlePrevPage()
            }
        },
        async details(row) {
            this.selectedRowData = row
            //console.log(this.selectedRowData)
            this.isShow = false
            this.isShowDetails = true
            this.detailTitle = '外币详情 - ' + this.selectedRowData.currency_name
            await this.getSimulationData()
            this.renderChart()
        },
        myTimeToLocal(inputTime){
            let res = inputTime.replace('T', ' ');
            res = res.replace('Z', '')
            return res;
        },
        async searchRecords(page) {
            this.tableData = []

            if(this.categoryCondition == '' && (this.maxDateCondition != '' || this.minDateCondition != '')) {
                ElMessage.warning("搜索外币选项为空时，无法对日期进行筛选")
                return
            }

            let queryParams = {}
            if(page != -1) {
                queryParams.curPage = page
                this.curPage = page
            }
            if(this.categoryCondition != '') {
                queryParams.categoryCondition = this.categoryCondition
            }
            if(this.maxDateCondition != '') {
                queryParams.maxDateCondition = this.maxDateCondition
            }
            if(this.minDateCondition != '') {[
                queryParams.minDateCondition = this.minDateCondition
            ]}

            await axios.get('/FExchange/user/currency/search', { params: queryParams })
                .then(response => {
                    //console.log(response.data)
                    if(response.data.error_num === 0) {
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
                        //console.log(response.data.msg)
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
        renderChart() {
            this.$nextTick(() => {
                const canvas = this.$refs.lineChart
                if (canvas) {
                    const ctx = canvas.getContext('2d')
                    if (ctx) {
                        this.chart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: this.simulationData.map(data => data.update_datetime),
                                datasets: [
                                    {
                                        label: '现汇买入价',
                                        data: this.simulationData.map(data => data.buying_rate),
                                        borderColor: this.simulationData.map((data, index) => index >= this.simulationData.length - 7 ? 'orange' : 'blue'),
                                        fill: false
                                    },
                                    {
                                        label: '现汇卖出价',
                                        data: this.simulationData.map(data => data.selling_rate),
                                        borderColor: this.simulationData.map((data, index) => index >= this.simulationData.length - 7 ? 'yellow' : 'green'),
                                        fill: false
                                    }
                                ]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false
                            }
                        })
                        //console.log(this.chart)
                    } else {
                        console.error('Canvas context is not available')
                    }
                } else {
                    console.error('Canvas element not found')
                }
            })
        },
        async getSimulationData() {
            this.simulationData = []
            //console.log(this.selectedRowData)
            await axios.get('/FExchange/user/currency/simulation', { params: { currency_id: this.selectedRowData.currency } })
                .then(response => {
                    //console.log(response.data)
                    if(response.data.error_num === 0) {
                        let datas = response.data.simulation_data
                        datas.forEach(element => {
                            const data = { buying_rate: 0, selling_rate: 0, update_datetime: '2024-06-01 00:00:00' }
                            data.buying_rate = element.buying_rate
                            data.selling_rate = element.selling_rate
                            data.update_datetime = element.update_datetime.slice(0, 10)
                            this.simulationData.push(data)
                        })
                    } else if(response.data.error_num === 2) {
                        ElMessage.warning("数据量过少，不支持模拟")
                    } else {
                        ElMessage.error("外汇数据请求错误")
                        console.log(response.data.msg)
                    }
                })
        }
    },
    mounted() {
        this.searchRecords(1)
        this.getAllCurrency()
    }
}
</script>