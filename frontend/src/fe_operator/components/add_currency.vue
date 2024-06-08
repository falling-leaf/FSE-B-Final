<template>
    <div style="text-align:center;  margin-top: 20px; font-size: 2em; font-weight: bold; ">新增外币
      </div>
    <div class="content-box">
    <h1 class="h11">新增外币名称：<input type="text" id="name" v-model="name" class="input"></h1>
    <h1 class="h11">最新买入价：<input type="text" id="latest_buy" v-model="latest_buy" class="input"></h1>
    <h1 class="h11">最新售出价：<input type="text" id="latest_sell" v-model="latest_sell" class="input"></h1>

    <el-button class="but"@click="handleConfirmAdd">确定添加</el-button>

    <el-button class="but" @click="Retreat">取消</el-button>
    </div>
  </template>
  
  <script >
  import {ref} from "vue"
  import {Delete, Edit, Plus, Search} from "@element-plus/icons-vue";
  import axios from "axios";
  
  export default {
    data () {
      return {
        foreign_exchange_operator_id: 1,
        isShow: true,
        currency_id : 1,
        person_id: 1,
        name: '',
        latest_buy: '',
        latest_sell: '',
        Edit,
        Delete,
        Search,
        Plus,
        selectedRowData: null,
        tableData: [{
                currency_name: '',
                latest_exchange_buying_rate: '',
                latest_exchange_selling_rate: ''
            }],
      }
    },
    created() {
      this.fetchDataFromUrl();
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
      async GetCurrency() {
        
      },
      Retreat() {
        this.$router.push('/FExchange/user/currency');
      },
      async handleConfirmAdd() {
        let addParams = {}
        if(this.name != '') {
            addParams.currency_name = this.name
        }
        if(this.latest_buy != '') {
          addParams.latest_exchange_buying_rate = this.latest_buy
        }
        if(this.latest_sell != '') {
          addParams.latest_exchange_selling_rate = this.latest_sell
        }
        addParams.operator_id= this.foreign_exchange_operator_id
        await axios.post('/FExchange/Operator/add', addParams)
          .then(response => {
            console.log(response.data);
            if (response.data.status === 'success') {
              ElMessage.warning('Currency add successfully');
            } else {
              alert('Error: ' + response.data.message);
            }
          })
        .catch(error => {
          ElMessage.warning('添加请求发送失败', error);
        });
        
      }
    }
  }
  </script>
  
  <style>
  .content-box {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  .h11{
    margin-left: 110px;
    color: #222222;
    font-size: medium;
    margin-top:30px;
    margin-bottom: 30px;
  }
  .but{
    color: aqua;
    margin-left: 110px;
    margin-right: 60px;
  }
  .input{
    margin-left: 20px;
    margin-bottom: 20px;
    font-size:medium;
    width:200px;
  }
  </style>